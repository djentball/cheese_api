from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from routes import cheese, categories, blogs
import logging

from db.database import database
from db.models_orm import Base
from db.database import engine


logging.basicConfig(level=logging.INFO)
uvicorn_access_logger = logging.getLogger("uvicorn.access")

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()

    yield

    await database.disconnect()

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(cheese.router)
app.include_router(categories.router)
app.include_router(blogs.router)
