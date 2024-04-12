from typing import Optional

from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import BaseModel, Field, EmailStr


class BaseUser(BaseModel):
    email: Optional[EmailStr] = Field(None)
    phone_number: str = Field(
        min_length=9, max_length=16, pattern=r'^\+\d{8,15}$'
    )
    username: Optional[str] = Field(None, min_length=5, max_length=32)
    about_me: Optional[str] = Field(None, min_length=1, max_length=300)


class UserRead(BaseUser, schemas.BaseUser[PydanticObjectId]):
    pass


class UserCreate(BaseUser, schemas.BaseUserCreate):
    class Config:
        json_schema_extra = {
            'example': {
                "email": "user@example.com",
                "phone_number": "+79999999999",
                "username": "username",
                "about_me": "about me info",
                "password": "password",
            },
        }


class UserUpdate(BaseUser, schemas.BaseUserUpdate):
    phone_number: Optional[str] = Field(
        None, min_length=9, max_length=16, pattern=r'^\+\d{8,15}$'
    )
