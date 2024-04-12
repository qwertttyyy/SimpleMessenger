from fastapi import APIRouter, Depends

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
)
async def filter_users(
    phone_number: str = None, email: str = None, username: str = None
):
    filters = {}
    if phone_number:
        filters['phone_number'] = {'$regex': f'^{phone_number}'}
    if email:
        filters['email'] = {'$regex': f'^{email}'}
    if username:
        filters['username'] = {'$regex': f'^{username}'}
    return await User.find(filters).to_list()
