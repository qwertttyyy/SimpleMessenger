from pathlib import Path

import jwt
from fastapi import WebSocket, APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.core.connection_manager import manager
from app.core.constants import MESSAGES_DEFAULT_LIMIT, MESSAGES_DEFAULT_OFFSET
from app.core.database import messages_collection
from app.core.users import current_user
from app.models import User
from app.schemas.messages import Message

router = APIRouter()


@router.get(
    "/messages/{receiver_id}",
    response_model=list[Message],
    dependencies=[Depends(current_user)],
    tags=['messages'],
    description='Получение списка сообщений пользователя '
    'отправленных пользователю с receiver_id',
)
async def get_messages(
    receiver_id: str,
    limit: int = MESSAGES_DEFAULT_LIMIT,
    offset: int = MESSAGES_DEFAULT_OFFSET,
    user=Depends(current_user),
):
    messages = await messages_collection.find(
        {'sender_id': str(user.id), 'receiver_id': receiver_id}
    ).to_list(limit)
    return messages[offset:]


@router.websocket("/ws/{receiver_id}/{token}")
async def websocket_endpoint(
    websocket: WebSocket, receiver_id: str, token: str
):
    """
    Эндпоинт WebSocket обрабатывает аутентификацию пользователя,
    управляет соединением WebSocket и обрабатывает входящие сообщения.
    """
    jwt_user = jwt.decode(
        token,
        settings.secret,
        algorithms=["HS256"],
        options={"verify_aud": False},
    )
    user = await User.get(jwt_user["sub"])
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")
    await manager.connect(user, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = Message(
                sender_id=user.id, receiver_id=receiver_id, content=data
            )
            await messages_collection.insert_one(message.dict())
            await manager.send_message(message)
    except Exception:
        await manager.disconnect(user)


@router.get("/chat", description='Страница чата')
def get_chat_page():
    templates = Path(__file__).resolve().parent.parent.parent / 'templates'
    with open(templates / 'chat.html') as file:
        content = file.read()
    return HTMLResponse(content)
