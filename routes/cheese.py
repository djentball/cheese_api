from fastapi import APIRouter, HTTPException, Query
from db import crud
from schemas import Cheese, CheeseListResponse

router = APIRouter(prefix="/cheese", tags=["Cheese"])


@router.post("/", response_model=Cheese)
async def create_cheese(cheese: Cheese):
    return await crud.create_cheese(cheese)


@router.get("/{cheese_id}", response_model=Cheese)
async def get_cheese(cheese_id: str):
    cheese = await crud.get_cheese_by_id(cheese_id)
    if cheese is None:
        raise HTTPException(status_code=404, detail="Cheese not found")
    return cheese


@router.put("/{cheese_id}", response_model=Cheese)
async def update_cheese(cheese_id: str, cheese: Cheese):
    existing_cheese = await crud.get_cheese_by_id(cheese_id)
    if existing_cheese is None:
        raise HTTPException(status_code=404, detail="Cheese not found")

    await crud.update_cheese(cheese_id, cheese)
    return await crud.get_cheese_by_id(cheese_id)


@router.delete("/{cheese_id}")
async def delete_cheese(cheese_id: str):
    deleted = await crud.delete_cheese(cheese_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cheese not found")
    return {"message": "Cheese deleted successfully"}


@router.get("/", response_model=CheeseListResponse)
async def get_cheeses(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return await crud.get_cheeses(limit, offset)
