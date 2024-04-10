from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.database import db
from app.models import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(
        database=db,
        document_models=[
            User,
        ],
    )
    yield


app = FastAPI(title=settings.app_title, lifespan=lifespan)
app.include_router(main_router)
