from typing import Optional, List

from beanie import Document
from pydantic import BaseModel


class CRUDBase:
    def __init__(self, collection: Document):
        self.collection = collection

    async def get(self, obj_id: str) -> Optional[Document]:
        return await self.collection.get(obj_id)

    async def get_list(self) -> List[Document]:
        return [doc async for doc in self.collection.find_all()]

    async def create(self, obj_in: BaseModel) -> Document:
        return await self.collection.insert_one(obj_in.dict())

    async def update(self, db_obj: Document, obj_in: BaseModel) -> Document:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await db_obj.replace()
        return db_obj

    async def remove(self, db_obj: Document) -> None:
        await db_obj.delete()
