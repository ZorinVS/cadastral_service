from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routers import checkhealth, query
from auth import routers as auth
from core.config import settings
from core.database import db


@asynccontextmanager
async def lifespan(application: FastAPI):
    await db.connect(dsn=settings.db_url)
    yield
    await db.disconnect()


app = FastAPI(
    title="Cadastral Service",
    lifespan=lifespan,
)

# Подключение роутеров
app.include_router(checkhealth.router)
app.include_router(query.router)
app.include_router(auth.router)
