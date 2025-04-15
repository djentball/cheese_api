from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from db.database import database
from routes import cheese, categories, blogs
from db.models_orm import Base
from db.database import engine
from admin.panel import register_admin
import logging

# Налаштування базового логування
logging.basicConfig(level=logging.INFO)
uvicorn_access_logger = logging.getLogger("uvicorn.access")

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan, root_path="/api")

# Підключення статики для SQLAdmin
app.mount(
    "/static",
    StaticFiles(directory="/home/api-aio/.local/lib/python3.12/site-packages/sqladmin/statics"),
    name="static"
)

# Реєстрація адмінки
register_admin(app, engine)

# Підключення CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутери
app.include_router(cheese.router)
app.include_router(categories.router)
app.include_router(blogs.router)
