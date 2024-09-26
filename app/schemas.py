from pydantic import BaseModel
from typing import Optional,List
import enum

# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

# Order Schemas
class OrderBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
class OrderStatus(str, enum.Enum):
    processing = "в процессе"
    shipped = "отправлен"
    delivered = "доставлен"
class OrderUpdateStatus(BaseModel):
    status: OrderStatus
class Order(OrderBase):
    id: int
    status: str

    class Config:
        orm_mode = True
