from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models_orm import Cheese, Blog, Category
from uuid import UUID
from typing import Optional, List, Sequence
from sqlalchemy import func


async def create_cheese(session: AsyncSession, cheese_data: dict) -> Cheese:
    new_cheese = Cheese(**cheese_data)
    session.add(new_cheese)
    await session.commit()
    await session.refresh(new_cheese)
    return new_cheese


async def get_cheese(session: AsyncSession, cheese_id: UUID) -> Optional[Cheese]:
    result = await session.execute(select(Cheese).where(Cheese.id == str(cheese_id)))
    return result.scalars().first()


async def get_all_cheeses(session: AsyncSession, limit: int = 10, offset: int = 0) -> Sequence[Cheese]:
    query = select(Cheese).order_by(Cheese.name).limit(limit).offset(offset)
    result = await session.execute(query)
    return result.scalars().all()


async def update_cheese(session: AsyncSession, cheese_id: UUID, cheese_data: dict) -> Optional[Cheese]:
    cheese = await get_cheese(session, cheese_id)
    if not cheese:
        return None
    for key, value in cheese_data.items():
        setattr(cheese, key, value)
    await session.commit()
    await session.refresh(cheese)
    return cheese


async def delete_cheese(session: AsyncSession, cheese_id: UUID) -> bool:
    cheese = await get_cheese(session, cheese_id)
    if not cheese:
        return False
    await session.delete(cheese)
    await session.commit()
    return True


async def create_category(session: AsyncSession, category_data: dict) -> Category:
    new_category = Category(**category_data)
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category


# 📥 Отримати категорію за ID
async def get_category(session: AsyncSession, category_id: UUID) -> Optional[Category]:
    result = await session.execute(select(Category).where(Category.id == str(category_id)))
    return result.scalars().first()


async def get_categories(session: AsyncSession, limit: int = 10, offset: int = 0) -> Sequence[Category]:
    query = select(Category).order_by(Category.name).limit(limit).offset(offset)
    result = await session.execute(query)
    categories = result.scalars().all()

    total_query = select(func.count()).select_from(Category)
    total_result = await session.execute(total_query)
    total = total_result.scalar()

    return total, categories


# ✏️ Оновити категорію
async def update_category(session: AsyncSession, category_id: UUID, category_data: dict) -> Optional[Category]:
    category = await get_category(session, category_id)
    if not category:
        return None
    for key, value in category_data.items():
        setattr(category, key, value)
    await session.commit()
    await session.refresh(category)
    return category


async def delete_category(session: AsyncSession, category_id: UUID) -> bool:
    category = await get_category(session, category_id)
    if not category:
        return False
    await session.delete(category)
    await session.commit()
    return True


async def get_cheeses_by_category(
        session: AsyncSession, category_id: UUID, limit: int = 10, offset: int = 0
) -> Sequence[Cheese]:
    print(f"Category ID type: {type(category_id)}")
    print(f"Category ID: {category_id}")

    print(f"Getting cheeses for category_id={category_id}, limit={limit}, offset={offset}")
    query = select(Cheese).where(Cheese.category_id == str(category_id)).limit(limit).offset(offset)

    print(f"SQL Query: {str(query)}")
    result = await session.execute(query)
    cheeses = result.scalars().all()
    print(f"Found cheeses: {cheeses}")

    total_query = select(func.count()).select_from(Cheese).where(Cheese.category_id == category_id)
    print(f"Total count query: {str(total_query)}")
    total_result = await session.execute(total_query)
    total = total_result.scalar()
    print(f"Total cheeses count: {total}")

    return total, cheeses


async def create_blog(session: AsyncSession, blog_data: dict) -> Blog:
    new_blog = Blog(**blog_data)
    session.add(new_blog)
    await session.commit()
    await session.refresh(new_blog)
    return new_blog


async def get_blog(session: AsyncSession, blog_id: UUID) -> Optional[Blog]:
    result = await session.execute(select(Blog).where(Blog.id == blog_id))
    return result.scalars().first()


async def get_all_blogs(session: AsyncSession, limit: int = 10, offset: int = 0) -> Sequence[Blog]:
    query = select(Blog).order_by(Blog.name).limit(limit).offset(offset)
    result = await session.execute(query)
    blogs = result.scalars().all()

    total_query = select(func.count()).select_from(Blog)
    total_result = await session.execute(total_query)
    total = total_result.scalar()

    return total, blogs


async def update_blog(session: AsyncSession, blog_id: UUID, blog_data: dict) -> Optional[Blog]:
    blog = await get_blog(session, blog_id)
    if not blog:
        return None
    for key, value in blog_data.items():
        setattr(blog, key, value)
    await session.commit()
    await session.refresh(blog)
    return blog


# Видалити блог
async def delete_blog(session: AsyncSession, blog_id: UUID) -> bool:
    blog = await get_blog(session, blog_id)
    if not blog:
        return False
    await session.delete(blog)
    await session.commit()
    return True
