from fastapi import FastAPI, Depends, Request, Form, status, HTTPException

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
import Order_CRUD
from schemas import OrderBase, OrderType, OrderUpdate

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("base.html",
                                      {"request": request})

@app.get("/customers")
def customers(request: Request, db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    return templates.TemplateResponse("customer.html",
                                      {"request": request, "customer_list": customers})

@app.get("/products")
def products(request: Request, db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return templates.TemplateResponse("product.html",
                                      {"request": request, "product_list": products})


@app.post("/product/add")
def add_product(request: Request, 
                    product_name: str = Form(...), 
                    price: str = Form(...), 
                    db: Session = Depends(get_db)):
    new_product = models.Product(product_name=product_name, price=price)
    db.add(new_product)
    db.commit()
    
    url = app.url_path_for("products")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.post("/customer/add")
def add_customer(request: Request, 
            name: str = Form(...), 
            db: Session = Depends(get_db)):
    new_customer = models.Customer(name=name)
    db.add(new_customer)
    db.commit()
    
    url = app.url_path_for("customers")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)



@app.get("/orders")
def orders(request: Request, db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return templates.TemplateResponse("order.html",
                                      {"request": request, "order_list": orders})

@app.post("/order/add")
def add_order(request: Request, 
            customer_id: int = Form(...), 
            product_id: int = Form(...), 
            amount: int = Form(...), 
            db: Session = Depends(get_db)):
    new_order = models.Order(customer_id=customer_id, product_id=product_id, amount=amount)
    db.add(new_order)
    db.commit()
    
    url = app.url_path_for("orders")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)



#############################################
#################    API    #################
#############################################


@app.get("/api/v1/orders", response_model=OrderType)
def read_orders(skip: int=0, limit: int=100, db:Session= Depends(get_db)):
    res = Order_CRUD.get_orders(db, skip, limit)
    response = {"skip":skip , "limit":limit , "data":res}
    return response

@app.get("/api/v1/order/{_id}", response_model=OrderUpdate)
def read_order(_id: int, db:Session= Depends(get_db)):
    res = Order_CRUD.get_order_by_id(db, _id)
    if res is None:
        raise HTTPException(status_code=404, detail="404 Not Found.")
    return res


@app.post("/api/v1/order", response_model=OrderUpdate)
def create_order(orderForm : OrderBase, db: Session = Depends(get_db)):
    try:
        res = Order_CRUD.create_order(db, orderForm)
        return res
    except Exception as err:
        raise HTTPException(**err.__dict__)


@app.put("/api/v1/order/{_id}", response_model=OrderUpdate)
def update_order(orderForm : OrderBase, _id:int, db: Session = Depends(get_db)):
    try:
        res = Order_CRUD.update_order(db, _id, orderForm)
        return res
    except Exception as err:
        raise HTTPException(**err.__dict__)
