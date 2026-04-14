from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Literal

from services.db import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    order_id = Column(String, index=True)
    marketplace = Column(String)
    product_name = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    cost_price = Column(Float)
    status = Column(String)
    sold_at = Column(Date)

class SaleBase(BaseModel):
    order_id: str
    marketplace: Literal['ozon', 'wildberries', 'yandex_market']
    product_name: str
    quantity: int
    price: float
    cost_price: float
    status: Literal['delivered', 'returned', 'cancelled']
    sold_at: date

    @field_validator('marketplace')
    def validate_marketplace(cls, v):
        if not v in ['ozon', 'wildberries', 'yandex_market']:
          raise ValueError('Маркетплейс должен быть одним из: ozon, wb, yandex market')
        return v

    @field_validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Цена должна быть положительной')
        return v

    @field_validator('cost_price')
    def validate_cost_price(cls, v):
        if v <= 0:
            raise ValueError('Себестоимость должна быть положительной')
        return v

    @field_validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Количество должно быть положительным')
        return v

    @field_validator('sold_at')
    def validate_sold_at(cls, v):
        if v > date.today():
            raise ValueError('Дата продажи не может быть в будущем')
        return v

class SaleCreate(SaleBase):
    pass

class SaleUpdate(SaleBase):
    pass

class SaleInDb(SaleBase):
    id: int

    class Config:
        from_attributes = True