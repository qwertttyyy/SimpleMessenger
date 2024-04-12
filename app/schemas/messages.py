from datetime import datetime

from beanie import PydanticObjectId

from pydantic import BaseModel, Field


class Message(BaseModel):
    sender_id: PydanticObjectId
    receiver_id: PydanticObjectId
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
