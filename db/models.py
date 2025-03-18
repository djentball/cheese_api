import uuid
from sqlalchemy import Table, Column, String, Float, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from db.database import metadata

cheese_table = Table(
    "cheeses",
    metadata,
    Column("id", String, primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("name", String, nullable=False),
    Column("country", String, nullable=False),
    Column("fat_content", Float, nullable=False),
    Column("age_months", Integer, nullable=False),
    Column("is_pasteurized", Boolean, nullable=False),
    Column("description", String, nullable=True),
)
