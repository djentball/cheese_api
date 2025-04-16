import uuid
from sqlalchemy import select, func, update, delete
from db.database import database
from db.models import cheese_table, categories_table, blogs_table
from schemas import Cheese, Categories, Blogs
from uuid import UUID


async def create_cheese(cheese: Cheese):
    query = cheese_table.insert().values(
        id=str(cheese.id) if cheese.id else str(uuid.uuid4()),
        name=cheese.name,
        country=cheese.country,
        fat_content=cheese.fat_content,
        age_months=cheese.age_months,
        is_pasteurized=cheese.is_pasteurized,
        description=cheese.description,
        image_url=cheese.image_url,
        category_id=str(cheese.category_id)  # Зберігаємо категорію
    )
    await database.execute(query)
    return cheese


async def get_cheeses_by_category(category_id: str, limit: int, offset: int):
    query = select(cheese_table).where(cheese_table.c.category_id == category_id).limit(limit).offset(offset)
    cheeses = await database.fetch_all(query)

    total_query = select(func.count()).where(cheese_table.c.category_id == category_id)
    total = await database.fetch_one(total_query)

    return {"total": total[0] if total else 0, "limit": limit, "offset": offset, "cheeses": cheeses}


async def get_cheese_by_id(cheese_id: str):
    query = select(cheese_table).where(cheese_table.c.id == cheese_id)
    return await database.fetch_one(query)


async def get_cheeses(limit: int, offset: int):
    query = select(cheese_table).limit(limit).offset(offset)
    cheeses = await database.fetch_all(query)

    total_query = select(func.count()).select_from(cheese_table)
    total = await database.fetch_one(total_query)

    return {"total": total[0] if total else 0, "limit": limit, "offset": offset, "cheeses": cheeses}


async def update_cheese(cheese_id: str, cheese_data: Cheese):
    cheese_dict = cheese_data.dict(exclude_unset=True)
    query = (
        update(cheese_table)
        .where(cheese_table.c.id == cheese_id)
        .values(**cheese_dict)
        .returning(cheese_table)
    )
    return await database.fetch_one(query)


async def delete_cheese(cheese_id: str):
    query = delete(cheese_table).where(cheese_table.c.id == cheese_id)
    await database.execute(query)


async def create_category(category: Categories):
    query = categories_table.insert().values(
        id=str(category.id) if category.id else str(uuid.uuid4()),  # Використовуємо наданий ID або генеруємо новий
        name=category.name,
        description=category.description,
        image_url=category.image_url
    )
    await database.execute(query)
    return category  # ✅ Повертаємо об'єкт із правильним UUID


async def get_category_by_id(category_id: str):
    query = select(categories_table).where(categories_table.c.id == category_id)
    return await database.fetch_one(query)


async def get_categories(limit: int, offset: int):
    query = select(categories_table).limit(limit).offset(offset)
    categories = await database.fetch_all(query)

    total_query = select(func.count()).select_from(categories_table)
    total = await database.fetch_one(total_query)

    return {"total": total[0] if total else 0, "limit": limit, "offset": offset, "categories": categories}


async def update_category(category_id: str, category_data: Categories):
    category_dict = category_data.dict(exclude_unset=True)
    query = (
        update(categories_table)
        .where(categories_table.c.id == category_id)
        .values(**category_dict)
        .returning(categories_table)  # Повертаємо оновлений запис
    )
    return await database.fetch_one(query)  # Повертаємо оновлений об'єкт


async def delete_category(category_id: str):
    query = delete(categories_table).where(categories_table.c.id == category_id)
    await database.execute(query)


# Blogs
async def create_blog(blog: Blogs):
    query = blogs_table.insert().values(
        id=str(blog.id) if blog.id else str(uuid.uuid4()),
        name=blog.name,
        short_description=blog.short_description,
        description=blog.description,
        image_url=blog.image_url
    )
    await database.execute(query)
    return blog


async def get_blog_by_id(blog_id: str):
    query = select(blogs_table).where(blogs_table.c.id == blog_id)
    return await database.fetch_one(query)


async def get_blogs(limit: int, offset: int):
    query = select(blogs_table).limit(limit).offset(offset)
    blogs = await database.fetch_all(query)

    total_query = select(func.count()).select_from(blogs_table)
    total = await database.fetch_one(total_query)

    return {"total": total[0] if total else 0, "limit": limit, "offset": offset, "blogs": blogs}


async def update_blog(blog_id: str, blog_data: Blogs):
    blog_dict = blog_data.dict(exclude_unset=True)
    query = (
        update(blogs_table)
        .where(blogs_table.c.id == blog_id)
        .values(**blog_dict)
        .returning(blogs_table)
    )
    return await database.fetch_one(query)


async def delete_blog(blog_id: str):
    query = delete(blogs_table).where(blogs_table.c.id == blog_id)
    await database.execute(query)