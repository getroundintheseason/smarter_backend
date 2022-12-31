from typing import List, Union
from pydantic import BaseModel
from uuid import UUID

class OrderBase(BaseModel):
    customer_id: int
    amount: int
    product_id: int

class OrderUpdate(OrderBase):
    id: int
    
    class Config:
        orm_mode = True

class OrderType(BaseModel):
    skip: int
    limit: int
    data: List[OrderUpdate]