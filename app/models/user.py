from typing import Optional

from beanie import Document
from fastapi_users_db_beanie import BeanieBaseUser
from pydantic import EmailStr


class User(BeanieBaseUser, Document):
    email: Optional[EmailStr] = None
    phone_number: str
