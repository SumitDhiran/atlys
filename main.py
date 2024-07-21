import json
from typing import Union
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database.models import Product, Base
from database.schemas import ProductResponseSchema, ProductSchema
from database.database import SessionLocal, engine
import redis
import soup

from fastapi import FastAPI, Body, Depends

from auth.auth_bearer import JWTBearer
from auth.auth_handler import sign_jwt

Base.metadata.create_all(bind=engine)

app = FastAPI()


# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@app.post("/scrape-products", dependencies=[Depends(JWTBearer())],)
async def scrape_products(url: str = None, page: int = None):
    status_code, err = soup.scrape(url, page)
    if status_code not in [200,201]:
        raise HTTPException(status_code, err)
    return status_code, err


@app.get("/products", response_model = ProductResponseSchema, dependencies=[Depends(JWTBearer())],)
async def get_products():
    r = redis.Redis(host='localhost', port=6379, db=0)
    data = r.get("products")
    data = json.loads(data)
    return {"status_code": 200, "data": data}