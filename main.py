from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from db.database import database
from routes import cheese, categories, blogs
from db.models_orm import Base
from db.database import engine
from admin.panel import register_admin

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan, root_path="/api")
# create_tables()


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

register_admin(app, engine)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="::", port=8355)
    # uvicorn.run(app)