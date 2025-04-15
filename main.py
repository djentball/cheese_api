from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import logging

from db.database import database
from db.models_orm import Base
from db.database import engine
from routes import cheese, categories, blogs
from admin.panel import register_admin

# ✅ RootPath Middleware для роботи SQLAdmin з reverse proxy
class RootPathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.scope["root_path"] = "/api"
        return await call_next(request)

# 🔧 Базове логування
logging.basicConfig(level=logging.INFO)
uvicorn_access_logger = logging.getLogger("uvicorn.access")

# 📦 Створюємо таблиці
Base.metadata.create_all(bind=engine)

# 🔄 Lifespan для підключення/відключення бази
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()

    print("🔧 Registering admin panel...")
    register_admin(app, engine)
    print("✅ Initializing SQLAdmin with base_url=/api/admin")

    # Вивід усіх маршрутів
    from fastapi.routing import APIRoute
    for route in app.routes:
        if isinstance(route, APIRoute):
            print(f"{route.path} -> {route.name}")

    yield
    await database.disconnect()


# 🚀 Створення FastAPI app
app = FastAPI(lifespan=lifespan, root_path="/api")

# 🔧 Примусово додаємо root_path, щоб SQLAdmin працював правильно
app.add_middleware(RootPathMiddleware)

# 📁 Підключення статики SQLAdmin
app.mount(
    "/static",  # НЕ додаємо /api
    StaticFiles(directory="/home/api-aio/.local/lib/python3.12/site-packages/sqladmin/statics"),
    name="static"
)

# 🌍 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔌 Підключення роутерів
app.include_router(cheese.router)
app.include_router(categories.router)
app.include_router(blogs.router)
