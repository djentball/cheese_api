import uuid
from sqlalchemy import select, func, update, delete
from db.database import database
from db.models import cheese_table, categories_table
from schemas import Cheese, Categories
from uuid import UUID


async def create_cheese(cheese: Cheese):
    query = cheese_table.insert().values(
        id=str(cheese.id) if cheese.id else str(uuid.uuid4()),  # Використовуємо наданий ID або генеруємо новий
        name=cheese.name,
        country=cheese.country,
        fat_content=cheese.fat_content,
        age_months=cheese.age_months,
        is_pasteurized=cheese.is_pasteurized,
        description=cheese.description,
        image_url=cheese.image_url
    )
    await database.execute(query)
    return cheese  # ✅ Повертаємо об'єкт із правильним UUID


async def get_cheese_by_id(cheese_id: UUID):
    query = select(cheese_table).where(cheese_table.c.id == cheese_id)
    return await database.fetch_one(query)


async def get_cheeses(limit: int, offset: int):
    query = select(cheese_table).limit(limit).offset(offset)
    cheeses = await database.fetch_all(query)

    total_query = select(func.count()).select_from(cheese_table)
    total = await database.fetch_one(total_query)

    return {"total": total[0] if total else 0, "limit": limit, "offset": offset, "cheeses": cheeses}


async def update_cheese(cheese_id: UUID, cheese_data: Cheese):
    cheese_dict = cheese_data.dict(exclude_unset=True)
    query = (
        update(cheese_table)
        .where(cheese_table.c.id == cheese_id)
        .values(**cheese_dict)
        .returning(cheese_table)  # Повертаємо оновлений запис
    )
    return await database.fetch_one(query)  # Повертаємо оновлений об'єкт


async def delete_cheese(cheese_id: UUID):
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


async def get_category_by_id(category_id: UUID):
    query = select(categories_table).where(categories_table.c.id == category_id)
    return await database.fetch_one(query)


async def get_categories(limit: int, offset: int):
    query = select(categories_table).limit(limit).offset(offset)
    categories = await database.fetch_all(query)

    total_query = select(func.count()).select_from(categories_table)
    total = await database.fetch_one(total_query)

    return {"total": total[0] if total else 0, "limit": limit, "offset": offset, "categories": categories}


async def update_category(category_id: UUID, category_data: Categories):
    category_dict = category_data.dict(exclude_unset=True)
    query = (
        update(categories_table)
        .where(categories_table.c.id == category_id)
        .values(**category_dict)
        .returning(categories_table)  # Повертаємо оновлений запис
    )
    return await database.fetch_one(query)  # Повертаємо оновлений об'єкт


async def delete_category(category_id: UUID):
    query = delete(categories_table).where(categories_table.c.id == category_id)
    await database.execute(query)
