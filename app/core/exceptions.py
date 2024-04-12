from typing import Any

from fastapi import HTTPException, status


class UserAlreadyExists(HTTPException):
    def __init__(self, detail: Any = None, headers: dict = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail if detail is not None else "User already exists",
            headers=headers,
        )
