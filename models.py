from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
import datetime
from database import Base
from fastapi.utils import generate_unique_id
from sqlalchemy_utils import UUIDType
import uuid

class Order(Base):
    __tablename__ = "orders"

    #id = Column(uuid, primary_key=True, index=True)
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(UUIDType(binary=False), default=uuid.uuid4)
    purchase_time = Column(DateTime, default=datetime.datetime.now())

    customer_id = Column(Integer, ForeignKey("customers.id"))
    amount = Column(Integer, default=False)
    product_id = Column(Integer, ForeignKey("products.id"))

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(UUIDType(binary=False), default=uuid.uuid4)
    create_time = Column(DateTime, default=datetime.datetime.now())    
    
    name = Column(String)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(UUIDType(binary=False), default=uuid.uuid4)
    create_time = Column(DateTime, default=datetime.datetime.now())   

    price = Column(Integer)
    product_name = Column(String)