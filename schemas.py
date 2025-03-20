from pydantic import BaseModel, Field
import uuid
from uuid import UUID
from typing import Optional, List


class Cheese(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, title="Унікальний ідентифікатор сиру")
    name: str
    country: str
    fat_content: float
    age_months: int
    is_pasteurized: bool
    description: Optional[str]
    image_url: str | None = None


class CheeseListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    cheeses: List[Cheese]


class Categories(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, title="Унікальний ідентифікатор категорії")
    name: str
    description: Optional[str]
    image_url: str | None = None


class CategoriesListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    categories: List[Categories]