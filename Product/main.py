from fastapi import FastAPI, status, Response, HTTPException
from .import schemas
from .import models 
from .database import engine , SessionLocal
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.delete('/product/{id}')
def delete(id, db:Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {'product deleted '}

@app.get('/products', response_model=List[schemas.DisplayProduct])
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.get('/product/{id}', response_model=schemas.DisplayProduct)
def products(id, response: Response, db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.id == id).first()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produt not found')
    return products

@app.put('/product/{id}')
def update(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id)
    if not product.first():
        pass
    product.update(request.dict())
    db.commit()
    return {'Product successfully updated'}

@app.post('/product', status_code=status.HTTP_201_CREATED)
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name,description=request.description,price=request.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request