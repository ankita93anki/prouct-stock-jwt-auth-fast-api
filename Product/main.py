from fastapi import FastAPI, status, Response, HTTPException
from .import schemas
from .import models 
from .database import engine , SessionLocal
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

app = FastAPI(
    title="Products API",
    description="Get details for all the products of on our website",
    terms_of_service="http://www.google.com",
    contact={
        "Developer name":"Ankita Singh",
        "website": "http://www.goog;e.com",
        "email":"demo@gmail.com"
    },
    license_info={
        "name":"XYZ",
        "url":"https://www.google.com"
    },
    docs_url="/documentation"
)

models.Base.metadata.create_all(engine)
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.delete('/product/{id}', tags=['Products'])
def delete(id, db:Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {'product deleted '}

@app.get('/products', response_model=List[schemas.DisplayProduct], tags=['Products'])
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.get('/product/{id}', response_model=schemas.DisplayProduct, tags=['Products'])
def products(id, response: Response, db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.id == id).first()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produt not found')
    return products

@app.put('/product/{id}', response_model=List[schemas.DisplayProduct],tags=['Products'])
def update(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id)
    if not product.first():
        pass
    product.update(request.dict())
    db.commit()
    return {'Product successfully updated'}

@app.post('/product', status_code=status.HTTP_201_CREATED, tags=['Products'])
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name,description=request.description,price=request.price, seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

@app.post('/seller', response_model=schemas.DisplaySeller, tags=['Sellers'])
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashedPassword = pwd_context.hash(request.password)
    new_seller = models.Seller(username=request.username, email=request.email, password=hashedPassword)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller