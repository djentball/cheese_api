from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.routing import APIRoute
import logging

from db.database import database
from routes import cheese, categories, blogs
from db.models_orm import Base
from db.database import engine
from admin.panel import register_admin


# Логування
logging.basicConfig(level=logging.INFO)
uvicorn_access_logger = logging.getLogger("uvicorn.access")

# Створення таблиць
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()

    print("🔧 Registering admin panel...")
    register_admin(app, engine)

    # Дебаг маршрутів
    for route in app.routes:
        if isinstance(route, APIRoute):
            print(f"{route.path} -> {route.name}")

    yield
    await database.disconnect()


# root_path потрібен для AlwaysData
app = FastAPI(lifespan=lifespan, root_path="/api")

# ⚠️ Шлях має бути /static, бо root_path вже додається автоматично
app.mount(
    "/static",
    StaticFiles(directory="/home/api-aio/.local/lib/python3.12/site-packages/sqladmin/statics"),
    name="static"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення маршрутів
app.include_router(cheese.router)
app.include_router(categories.router)
app.include_router(blogs.router)
