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

# Логування доступу до API (uvicorn access логгер)
uvicorn_access_logger = logging.getLogger("uvicorn.access")


Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()

    from admin.panel import register_admin
    from db.database import engine
    register_admin(app, engine)

    from fastapi.routing import APIRoute
    for route in app.routes:
        if isinstance(route, APIRoute):
            print(f"{route.path} -> {route.name}")

    yield

    await database.disconnect()

app = FastAPI(lifespan=lifespan, root_path="/api")
app.mount(
    "/static",  # <- без /api
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


app.include_router(cheese.router)
app.include_router(categories.router)
app.include_router(blogs.router)

# register_admin(app, engine)


# if __name__ == '__main__':
#     import uvicorn
#
#     uvicorn.run(app, host="::", port=8355)
    # uvicorn.run(app)