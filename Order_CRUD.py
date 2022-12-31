from typing import List
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session, session
from models import Product, Customer, Order
from schemas import OrderUpdate

def get_order_by_id(boxSession: Session, _id: int):
    return boxSession.query(Order).filter(Order.id == _id).first()

def get_product_by_id(boxSession: Session, _id: int):
    return boxSession.query(Product).filter(Product.id == _id).first()

def get_customer_by_id(boxSession: Session, _id: int):
    return boxSession.query(Customer).filter(Customer.id == _id).first()

def get_orders(boxSession: Session, _skip: int=0, _limit: int=100) -> List[Order]:
    return boxSession.query(Order).offset(_skip).limit(_limit).all()

def create_order(boxSession: Session, _createData: OrderUpdate) -> Order :
    orderProduct = get_product_by_id(boxSession, int(_createData.product_id))
    if orderProduct is None:
        raise HTTPException(status_code=409, detail="Order product_id do not exist!!")

    orderCustomer = get_customer_by_id(boxSession, int(_createData.customer_id))
    if orderCustomer is None:
        raise HTTPException(status_code=409, detail="Order customer_id do not exist!!")
    
    newOrder = Order(**_createData.dict())
    boxSession.add(newOrder)
    boxSession.commit()
    boxSession.refresh(newOrder)
    return newOrder

def update_order(boxSession: Session, _id: int, _updateData: OrderUpdate) -> Order:
    orderProduct = get_product_by_id(boxSession, int(_updateData.product_id))
    if orderProduct is None:
        raise HTTPException(status_code=409, detail="Order product_id do not exist!!")

    orderCustomer = get_customer_by_id(boxSession, int(_updateData.customer_id))
    if orderCustomer is None:
        raise HTTPException(status_code=409, detail="Order customer_id do not exist!!")

    orignalOrder = get_order_by_id(boxSession, _id)
    if orignalOrder is None:
        raise HTTPException(status_code=404 , detail="404 Not Found.")

    if orignalOrder.customer_id != _updateData.customer_id:
        raise HTTPException(status_code=409, detail="form customer_id conflict with original order.customer_id!!")

    orignalOrder.product_id = _updateData.product_id
    orignalOrder.amount = _updateData.amount

    boxSession.commit()
    boxSession.refresh(orignalOrder)

    return orignalOrder
