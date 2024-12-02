from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from src.database.base import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(511))
    price = Column(DECIMAL(10, 2), nullable=False)
    inventory = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    category_id = Column(Integer, ForeignKey("category.id"))

    category = relationship("Category", back_populates="products")


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(127))

    products = relationship("Product", back_populates="category")
