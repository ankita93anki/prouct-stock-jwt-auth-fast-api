from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..database import get_db
from ..import models, schemas
from typing import List
from fastapi import FastAPI, status, Response, HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from fastapi import status
from Product.routers.login import get_current_user

router = APIRouter(
    tags=['Products'],
    prefix="/products")

@router.delete('/{id}')
def delete(id, db:Session = Depends(get_db), current_user:schemas.Seller = Depends(get_current_user)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {'product deleted '}

@router.get('/', response_model=List[schemas.DisplayProduct])
def products(db: Session = Depends(get_db), current_user:schemas.Seller = Depends(get_current_user)):
    products = db.query(models.Product).all()
    return products

@router.get('/{id}', response_model=schemas.DisplayProduct)
def products(id, response: Response, db: Session = Depends(get_db), current_user:schemas.Seller = Depends(get_current_user)):
    products = db.query(models.Product).filter(models.Product.id == id).first()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produt not found')
    return products

@router.put('/{id}', response_model=List[schemas.DisplayProduct])
def update(id, request: schemas.Product, db: Session = Depends(get_db), current_user:schemas.Seller = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id)
    if not product.first():
        pass
    product.update(request.dict())
    db.commit()
    return {'Product successfully updated'}

@router.post('/', status_code=status.HTTP_201_CREATED)
def add(request: schemas.Product, db: Session = Depends(get_db), current_user:schemas.Seller = Depends(get_current_user)):
    new_product = models.Product(name=request.name,description=request.description,price=request.price, seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request