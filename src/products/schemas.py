from datetime import datetime
from typing import Optional

from pydantic import BaseModel, condecimal, field_validator

from src.products.validators import validate_name, validate_price, validate_inventory

price_dec = condecimal(max_digits=10, decimal_places=2)


class ProductBase(BaseModel):
    name: str
    description: str
    price: price_dec
    inventory: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str):
        validate_name(name)
        return name

    @field_validator("price")
    @classmethod
    def validate_price(cls, price: price_dec):
        validate_price(price)
        return price

    @field_validator("inventory")
    @classmethod
    def validate_inventory(cls, inventory: int):
        validate_inventory(inventory)
        return inventory


class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductPartialUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[price_dec] = None
    inventory: Optional[int] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str):
        validate_name(name)
        return name

    @field_validator("price")
    @classmethod
    def validate_price(cls, price: price_dec):
        validate_price(price)
        return price

    @field_validator("inventory")
    @classmethod
    def validate_inventory(cls, inventory: int):
        validate_inventory(inventory)
        return inventory
