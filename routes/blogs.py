from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from db import crud_orm as crud
from db.database import get_db
from schemas import Blogs, BlogsListResponse

router = APIRouter(prefix="/blog", tags=["Blogs"])


@router.post("/", response_model=Blogs)
async def create_blog_route(blog: Blogs, db: AsyncSession = Depends(get_db)):
    return await crud.create_blog(db, blog.dict())


@router.get("/{blog_id}", response_model=Blogs)
async def get_blog_route(blog_id: UUID, db: AsyncSession = Depends(get_db)):
    blog = await crud.get_blog(db, blog_id)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.put("/{blog_id}", response_model=Blogs)
async def update_blog_route(blog_id: UUID, blog: Blogs, db: AsyncSession = Depends(get_db)):
    existing_blog = await crud.get_blog(db, blog_id)
    if existing_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    return await crud.update_blog(db, blog_id, blog.dict(exclude_unset=True))


@router.delete("/{blog_id}")
async def delete_blog_route(blog_id: UUID, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_blog(db, blog_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}


@router.get("/", response_model=BlogsListResponse)
async def get_blogs_route(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    total, blogs = await crud.get_all_blogs(db, limit=limit, offset=offset)
    return BlogsListResponse(
        total=total,
        limit=limit,
        offset=offset,
        blogs=blogs
    )
