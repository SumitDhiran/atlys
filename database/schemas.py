from typing import List
from pydantic import BaseModel



class ProductSchema(BaseModel):
    product_title: str
    product_price: str
    path_to_image: str

    class Config:
        from_attributes = True

class ProductResponseSchema(BaseModel):
    status_code: int
    data: List[ProductSchema]