from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from db.database import database, create_tables
from routes import cheese, categories, blogs


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
create_tables()


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


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)