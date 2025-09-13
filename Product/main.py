from fastapi import FastAPI
from .import models 
from .database import engine
from .routers import product,seller,login

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
app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)
models.Base.metadata.create_all(engine)

