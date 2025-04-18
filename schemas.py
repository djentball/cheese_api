from pydantic import BaseModel, Field
from typing import Optional, List
import uuid


# === BASE ===

class CheeseBase(BaseModel):
    name: str
    country: str
    fat_content: float
    age_months: int
    is_pasteurized: bool
    description: Optional[str] = None
    image_url: Optional[str] = None
    category_id: str


# === CREATE ===

class CheeseCreate(CheeseBase):
    pass


# === UPDATE ===

class CheeseUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    fat_content: Optional[float] = None
    age_months: Optional[int] = None
    is_pasteurized: Optional[bool] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[str] = None


# === RESPONSE ===

class Cheese(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    country: str
    fat_content: float
    age_months: int
    is_pasteurized: bool
    description: Optional[str] = None
    image_url: Optional[str] = None
    category_id: str

    class Config:
        from_attributes = True


class CheeseListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    cheeses: List[Cheese]


# ==== Category ====

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class Categories(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

class CategoriesListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    categories: List[Categories]


# ==== Blog ====

class BlogBase(BaseModel):
    name: str
    short_description: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BaseModel):
    name: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class Blogs(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    short_description: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

class BlogsListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    blogs: List[Blogs]
