from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List


class Cheese(BaseModel):
    id: UUID = Field(default_factory=UUID, title="Унікальний ідентифікатор сиру")
    name: str
    country: str
    fat_content: float
    age_months: int
    is_pasteurized: bool
    description: Optional[str]


class CheeseListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    cheeses: List[Cheese]
