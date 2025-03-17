import uuid
from sqlalchemy import select
from .database import database
from .models import cheese_table
from ..schemas import Cheese  # Імпортуємо Pydantic-схему

async def create_cheese(cheese: Cheese):
    query = cheese_table.insert().values(
        id=str(uuid.uuid4()),
        name=cheese.name,
        country=cheese.country,
        fat_content=cheese.fat_content,
        age_months=cheese.age_months,
        is_pasteurized=cheese.is_pasteurized,
        description=cheese.description
    )
    await database.execute(query)

async def get_cheese_by_id(cheese_id: str):
    query = select(cheese_table).where(cheese_table.c.id == cheese_id)
    return await database.fetch_one(query)

async def get_cheeses(limit: int, offset: int):
    query = select(cheese_table).limit(limit).offset(offset)
    cheeses = await database.fetch_all(query)
    total_query = select([cheese_table]).count()
    total = await database.execute(total_query)
    return {"total": total, "limit": limit, "offset": offset, "cheeses": cheeses}
