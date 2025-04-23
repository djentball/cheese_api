from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from routes import cheese, categories, blogs, auth
import logging

from db.database import engine, create_tables

logging.basicConfig(level=logging.INFO)
uvicorn_access_logger = logging.getLogger("uvicorn.access")


@asynccontextmanager
async def lifespan(app: FastAPI):

    await create_tables()

    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(cheese.router)
app.include_router(categories.router)
app.include_router(blogs.router)
