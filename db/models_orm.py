
import uuid

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, Boolean, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Cheese(Base):
    __tablename__ = "cheeses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    country = Column(String)
    fat_content = Column(Float)
    age_months = Column(Integer)
    is_pasteurized = Column(Boolean)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    category_id = Column(String, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="cheeses")


class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    cheeses = relationship("Cheese", back_populates="category")

    def __str__(self):
        return self.name  # 👈 Ось це і є ключовий момент

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    short_description = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)