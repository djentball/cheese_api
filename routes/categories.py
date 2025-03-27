from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from db import crud
from schemas import Categories, CategoriesListResponse, CheeseListResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=Categories)
async def create_category(category: Categories):
    return await crud.create_category(category)


@router.get("/{category_id}", response_model=Categories)
async def get_category(category_id: str):
    category = await crud.get_category_by_id(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=Categories)
async def update_category(category_id: str, category: Categories):
    existing_category = await crud.get_category_by_id(category_id)
    if existing_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    await crud.update_category(category_id, category)
    return await crud.get_category_by_id(category_id)


@router.delete("/{category_id}")
async def delete_category(category_id: str):
    deleted = await crud.delete_category(category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}


@router.get("/", response_model=CategoriesListResponse)
async def get_categories(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return await crud.get_categories(limit, offset)


@router.get("/{category_id}/cheeses", response_model=CheeseListResponse)
async def get_cheeses_by_category(category_id: str, limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    return await crud.get_cheeses_by_category(category_id, limit, offset)