from pydantic import BaseModel

#pydantic model
class Product(BaseModel):
    name: str 
    description: str 
    price:  int

class DisplayProduct(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True