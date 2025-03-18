from fastapi import FastAPI, HTTPException, Query
from typing import List, Union
from uuid import UUID
from db.database import database
from db import crud
from schemas import Cheese, CheeseListResponse
from contextlib import asynccontextmanager
from db.database import database, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
create_tables()


@app.post("/cheese/", response_model=Cheese)
async def create_cheese(cheese: Cheese):
    await crud.create_cheese(cheese)
    return cheese


@app.get("/cheese/{cheese_id}", response_model=Cheese)
async def get_cheese(cheese_id: UUID):
    cheese = await crud.get_cheese_by_id(str(cheese_id))
    if cheese is None:
        raise HTTPException(status_code=404, detail="Cheese not found")
    return cheese


@app.get("/cheese/", response_model=CheeseListResponse)
async def get_cheeses(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return await crud.get_cheeses(limit, offset)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)