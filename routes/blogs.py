from fastapi import APIRouter, HTTPException, Query
from db import crud
from schemas import Blogs, BlogsListResponse

router = APIRouter(prefix="/blog", tags=["Blogs"])


@router.post("/", response_model=Blogs)
async def create_blog(blog: Blogs):
    return await crud.create_blog(blog)


@router.get("/{blog_id}", response_model=Blogs)
async def get_blog(blog_id: str):
    blog = await crud.get_blog_by_id(blog_id)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.put("/{blog_id}", response_model=Blogs)
async def update_blog(blog_id: str, blog: Blogs):
    existing_blog = await crud.get_blog_by_id(blog_id)
    if existing_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    await crud.update_blog(blog_id, blog)
    return await crud.get_blog_by_id(blog_id)


@router.delete("/{blog_id}")
async def delete_blog(blog_id: str):
    deleted = await crud.delete_blog(blog_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}


@router.get("/", response_model=BlogsListResponse)
async def get_blogs(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return await crud.get_blogs(limit, offset)
