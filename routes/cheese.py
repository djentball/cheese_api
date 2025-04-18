from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from db import crud_orm as crud
from schemas import CheeseCreate, CheeseUpdate, Cheese, CheeseListResponse
from uuid import UUID

router = APIRouter(prefix="/cheese", tags=["Cheese"])


@router.post("/", response_model=Cheese)
async def create_cheese(
        cheese: CheeseCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_cheese(db, cheese.dict())


@router.get("/{cheese_id}", response_model=Cheese)
async def get_cheese(
        cheese_id: UUID,
        db: AsyncSession = Depends(get_db)
):
    cheese = await crud.get_cheese(db, cheese_id)
    if cheese is None:
        raise HTTPException(status_code=404, detail="Cheese not found")
    return cheese


@router.put("/{cheese_id}", response_model=Cheese)
async def update_cheese(
        cheese_id: UUID,
        cheese: CheeseUpdate,
        db: AsyncSession = Depends(get_db)
):
    existing_cheese = await crud.get_cheese(db, cheese_id)
    if existing_cheese is None:
        raise HTTPException(status_code=404, detail="Cheese not found")

    updated = await crud.update_cheese(db, cheese_id, cheese.dict(exclude_unset=True))
    return updated


@router.delete("/{cheese_id}")
async def delete_cheese(
        cheese_id: UUID,
        db: AsyncSession = Depends(get_db)
):
    deleted = await crud.delete_cheese(db, cheese_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cheese not found")
    return {"message": "Cheese deleted successfully"}


@router.get("/", response_model=CheeseListResponse)
async def get_cheeses(
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        db: AsyncSession = Depends(get_db)
):
    cheeses = await crud.get_all_cheeses(db, limit=limit, offset=offset)
    return CheeseListResponse(total=len(cheeses), limit=limit, offset=offset, cheeses=cheeses)