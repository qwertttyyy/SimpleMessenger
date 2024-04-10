from typing import Optional

from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import EmailStr, Field


class BaseUser:
    pass


class UserRead(schemas.BaseUser[PydanticObjectId]):
    email: Optional[EmailStr] = Field(None)
    phone_number: str = Field(
        min_length=9, max_length=15, pattern=r'^\+\d{8,15}$'
    )


class UserCreate(schemas.BaseUserCreate):
    email: Optional[EmailStr] = Field(None)
    phone_number: str = Field(
        min_length=9, max_length=15, pattern=r'^\+\d{8,15}$'
    )

    class Config:
        json_schema_extra = {
            'example': {
                'phone_number': '+89998887766',
                'password': 'qweasd123',
            }
        }


class UserUpdate(schemas.BaseUserUpdate):
    email: Optional[EmailStr] = Field(None)
    phone_number: str = Field(
        min_length=9, max_length=15, pattern=r'^\+\d{8,15}$'
    )
