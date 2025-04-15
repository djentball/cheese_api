from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.routing import APIRoute
from sqladmin import Admin

import logging

from db.database import database
from db.models_orm import Base
from db.database import engine
from admin.panel import CheeseAdmin, CategoryAdmin, BlogAdmin


# Базове логування
logging.basicConfig(level=logging.INFO)
uvicorn_access_logger = logging.getLogger("uvicorn.access")

# Створюємо таблиці (для SQLite та інших)
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()

    # Ініціалізуємо SQLAdmin з урахуванням root_path
    print("🔧 Registering admin panel...")
    admin = Admin(app=app, engine=engine, base_url="/api/admin")
    print("✅ Initializing SQLAdmin with base_url=/api/admin")
    admin.add_view(CheeseAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(BlogAdmin)

    # Виводимо всі маршрути для дебагу
    for route in app.routes:
        if isinstance(route, APIRoute):
            print(f"{route.path} -> {route.name}")

    yield

    await database.disconnect()

# Створюємо FastAPI з root_path, потрібним для reverse proxy
app = FastAPI(lifespan=lifespan, root_path="/api")

# Статика SQLAdmin
app.mount(
    "/api/static",
    StaticFiles(directory="/home/api-aio/.local/lib/python3.12/site-packages/sqladmin/statics"),
    name="static"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення роутів
from routes import cheese, categories, blogs
app.include_router(cheese.router)
app.include_router(categories.router)
app.include_router(blogs.router)
