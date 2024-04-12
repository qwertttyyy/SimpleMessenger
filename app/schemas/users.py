from typing import Optional

from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import BaseModel, Field, EmailStr, AnyUrl

from app.core.constants import (
    PHONE_NUMBER_REGULAR_PATTERN,
    MIN_USERNAME_LENGTH,
    MAX_USERNAME_LENGTH,
    MAX_ABOUT_ME_LENGTH,
    MIN_ABOUT_ME_LENGTH,
)


class BaseUser(BaseModel):
    email: Optional[EmailStr] = Field(None)
    phone_number: str = Field(
        min_length=9, max_length=16, pattern=PHONE_NUMBER_REGULAR_PATTERN
    )
    username: Optional[str] = Field(
        None, min_length=MIN_USERNAME_LENGTH, max_length=MAX_USERNAME_LENGTH
    )
    about_me: Optional[str] = Field(
        None, min_length=MIN_ABOUT_ME_LENGTH, max_length=MAX_ABOUT_ME_LENGTH
    )


class UserRead(BaseUser, schemas.BaseUser[PydanticObjectId]):
    avatar_url: Optional[AnyUrl] = Field(None)


class UserCreate(BaseUser, schemas.BaseUserCreate):
    class Config:
        json_schema_extra = {
            'example': {
                "phone_number": "+79999999999",
                "password": "password",
            },
        }


class UserUpdate(BaseUser, schemas.BaseUserUpdate):
    phone_number: Optional[str] = Field(
        None, min_length=9, max_length=16, pattern=r'^\+\d{8,15}$'
    )

    class Config:
        json_schema_extra = {
            'example': {
                "email": "user@example.com",
                "phone_number": "+79999999999",
                "username": "username",
                "about_me": "about me info",
            },
        }
