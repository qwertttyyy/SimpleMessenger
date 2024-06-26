import datetime
import shutil
import time

from fastapi import APIRouter, Depends, UploadFile, File
from pydantic import BaseModel

from app.core.config import settings
from app.core.users import fastapi_users, auth_backend, current_user
from app.models import User
from app.schemas.users import UserCreate, UserRead, UserUpdate

router = APIRouter()
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@router.get(
    '/users/',
    response_model=list[UserRead],
    dependencies=[Depends(current_user)],
    tags=['users'],
    description='Получение списка пользователей с фильтрацией по '
    'номеру телефона, почте и юзернейму',
)
async def filter_users(
    phone_number: str = None, email: str = None, username: str = None
) -> list[BaseModel]:
    filters = {}
    if phone_number:
        filters['phone_number'] = {'$regex': f'^{phone_number}'}
    if email:
        filters['email'] = {'$regex': f'^{email}'}
    if username:
        filters['username'] = {'$regex': f'^{username}'}
    return await User.find(filters).to_list()


@router.post(
    '/users/avatar',
    dependencies=[Depends(current_user)],
    description='Обновление аватара пользователя',
)
async def upload_avatar(
    avatar: UploadFile = File(...), user: User = Depends(current_user)
):
    filename = f'{user.id}_{int(time.time())}_{avatar.filename}'
    avatar_path = settings.media_folder / filename

    with open(avatar_path, 'wb') as buffer:
        shutil.copyfileobj(avatar.file, buffer)

    avatar_url = f"{settings.base_url}:{settings.port}/media/{filename}"
    user.avatar_url = avatar_url
    await user.save()
    return {'avatar_url': avatar_url}
