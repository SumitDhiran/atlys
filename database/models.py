from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    product_title = Column(String)
    product_price = Column(String)
    path_to_image = Column(String)
