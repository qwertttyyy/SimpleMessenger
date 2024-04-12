from typing import Optional

from beanie import Document
from fastapi_users_db_beanie import BeanieBaseUser
from pydantic import EmailStr, AnyUrl, Field


class User(BeanieBaseUser, Document):
    email: Optional[EmailStr] = None
    phone_number: str
    username: Optional[str] = None
    about_me: Optional[str] = None
    avatar_url: Optional[AnyUrl] = Field(None)
