from typing import Dict

from beanie import PydanticObjectId
from fastapi import WebSocket
from starlette.websockets import WebSocketState

from app.models import User
from app.schemas.messages import Message


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[PydanticObjectId, WebSocket] = {}

    async def connect(self, user: User, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user.id] = websocket

    async def disconnect(self, user: User):
        websocket = self.active_connections.pop(user.id)
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close()

    async def send_message(self, message: Message):
        if message.receiver_id in self.active_connections:
            await self.active_connections[message.receiver_id].send_text(
                message.content
            )


manager = ConnectionManager()
