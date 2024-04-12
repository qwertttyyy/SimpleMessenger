from typing import Optional, Union, Dict, Any

from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import (
    FastAPIUsers,
    BaseUserManager,
    InvalidPasswordException,
    schemas,
    models,
    exceptions,
)
from fastapi_users.authentication import (
    BearerTransport,
    JWTStrategy,
    AuthenticationBackend,
)
from fastapi_users_db_beanie import (
    BeanieUserDatabase,
    UP_BEANIE,
    ObjectIDIDMixin,
)

from app.core.config import settings
from app.core.exceptions import UserAlreadyExists
from app.models.user import User
from app.schemas.users import UserCreate


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = settings.secret
    verification_token_secret = settings.secret

    async def get_user_by_phone_number(
        self, phone_number: str
    ) -> Optional[UP_BEANIE]:
        user = self.user_db.user_model
        return await user.find_one(user.phone_number == phone_number)

    async def get_user_by_email(self, email: str) -> Optional[UP_BEANIE]:
        user = self.user_db.user_model
        return await user.find_one(user.email == email)

    async def get_user_by_username(self, username: str) -> Optional[UP_BEANIE]:
        user = self.user_db.user_model
        return await user.find_one(user.username == username)

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        if await self.get_user_by_phone_number(user_create.phone_number):
            raise UserAlreadyExists(
                'User with this phone number already exists'
            )

        if user_create.email and await self.get_user_by_email(
            user_create.email
        ):
            raise UserAlreadyExists('User with this email already exists')

        if user_create.username and await self.get_user_by_username(
            user_create.username
        ):
            raise UserAlreadyExists('User with this username already exists')

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        created_user = await self.user_db.create(user_dict)
        await self.on_after_register(created_user, request)
        return created_user

    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[models.UP]:

        user = await self.get_user_by_phone_number(credentials.username)
        if user is None:
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = (
            self.password_helper.verify_and_update(
                credentials.password, user.hashed_password
            )
        )
        if not verified:
            return None

        if updated_password_hash is not None:
            await self.user_db.update(
                user, {"hashed_password": updated_password_hash}
            )

        return user

    async def _update(
        self, user: models.UP, update_dict: Dict[str, Any]
    ) -> models.UP:
        validated_update_dict = {}
        for field, value in update_dict.items():
            if field == "email" and value != user.email:
                try:
                    await self.get_by_email(value)
                    raise exceptions.UserAlreadyExists()
                except exceptions.UserNotExists:
                    validated_update_dict["email"] = value
                    validated_update_dict["is_verified"] = False
            elif field == "password" and value is not None:
                await self.validate_password(value, user)
                validated_update_dict["hashed_password"] = (
                    self.password_helper.hash(value)
                )
            elif field == "username" and value is not None:
                if await self.get_user_by_username(value):
                    raise UserAlreadyExists(
                        'User with this username already exists'
                    )
            elif field == "phone_number" and value is not None:
                if await self.get_user_by_phone_number(value):
                    raise UserAlreadyExists(
                        'User with phone number already exists'
                    )
            else:
                validated_update_dict[field] = value
        return await self.user_db.update(user, validated_update_dict)

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(
            f"User {user.id} has forgot their password. Reset token: {token}"
        )

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )


async def get_user_db():
    yield BeanieUserDatabase(User)


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](
    get_user_manager, [auth_backend]
)

current_user = fastapi_users.current_user(active=True)
