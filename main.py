from fastapi import FastAPI, HTTPException, Query
from typing import List, Union
from uuid import UUID
from db.database import database
from db import crud
from schemas import Cheese, CheeseListResponse, Categories, CategoriesListResponse
from contextlib import asynccontextmanager
from db.database import database, create_tables
from fastapi.middleware.cors import CORSMiddleware


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


@app.post("/cheese/", response_model=Cheese)
async def create_cheese(cheese: Cheese):
    return await crud.create_cheese(cheese)


@app.get("/cheese/{cheese_id}", response_model=Cheese)
async def get_cheese(cheese_id: UUID):
    cheese = await crud.get_cheese_by_id(cheese_id)
    if cheese is None:
        raise HTTPException(status_code=404, detail="Cheese not found")
    return cheese


@app.put("/cheese/{cheese_id}", response_model=Cheese)
async def update_cheese(cheese_id: UUID, cheese: Cheese):
    existing_cheese = await crud.get_cheese_by_id(cheese_id)
    if existing_cheese is None:
        raise HTTPException(status_code=404, detail="Cheese not found")

    await crud.update_cheese(cheese_id, cheese)
    return await crud.get_cheese_by_id(cheese_id)


@app.delete("/cheese/{cheese_id}")
async def delete_cheese(cheese_id: UUID):
    deleted = await crud.delete_cheese(cheese_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cheese not found")
    return {"message": "Cheese deleted successfully"}


@app.get("/cheese/", response_model=CheeseListResponse)
async def get_cheeses(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return await crud.get_cheeses(limit, offset)


@app.post("/categories/", response_model=Categories)
async def create_category(category: Categories):
    return await crud.create_category(category)


@app.get("/categories/{category_id}", response_model=Categories)
async def get_category(category_id: UUID):
    category = await crud.get_category_by_id(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.put("/categories/{category_id}", response_model=Categories)
async def update_category(category_id: UUID, category: Categories):
    existing_category = await crud.get_category_by_id(category_id)
    if existing_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    await crud.update_category(category_id, category)
    return await crud.get_category_by_id(category_id)


@app.delete("/categories/{category_id}")
async def delete_category(category_id: UUID):
    deleted = await crud.delete_category(category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}


@app.get("/categories/", response_model=CategoriesListResponse)
async def get_categories(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return await crud.get_categories(limit, offset)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)