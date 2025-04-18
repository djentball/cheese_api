from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from db import crud_orm as crud
from db.database import get_db
from schemas import (
    CategoryCreate,
    CategoryUpdate,
    Categories,
    CategoriesListResponse,
    CheeseListResponse
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=Categories)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_category(db, category.dict())


@router.get("/{category_id}", response_model=Categories)
async def get_category(category_id: UUID, db: AsyncSession = Depends(get_db)):
    category = await crud.get_category_by_id(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=Categories)
async def update_category(category_id: UUID, category: CategoryUpdate, db: AsyncSession = Depends(get_db)):
    existing_category = await crud.get_category_by_id(db, category_id)
    if existing_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return await crud.update_category(db, category_id, category.dict(exclude_unset=True))


@router.delete("/{category_id}")
async def delete_category(category_id: UUID, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}


@router.get("/", response_model=CategoriesListResponse)
async def get_categories(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    total, categories = await crud.get_categories(db, limit=limit, offset=offset)
    return CategoriesListResponse(
        total=total,
        limit=limit,
        offset=offset,
        categories=categories
    )


@router.get("/{category_id}/cheeses", response_model=CheeseListResponse)
async def get_cheeses_by_category(
    category_id: UUID,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    total, cheeses = await crud.get_cheeses_by_category(db, category_id, limit, offset)
    return CheeseListResponse(
        total=total,
        limit=limit,
        offset=offset,
        cheeses=cheeses
    )
