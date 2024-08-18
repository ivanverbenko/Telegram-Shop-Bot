from imghdr import tests

from sqlalchemy import Column, Integer, BigInteger, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from database.database import Base


class Category(Base):
    __tablename__ = 'category'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String)

class Product(Base):
    __tablename__ = 'product'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String)
    price:Mapped[float] = mapped_column(Float)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))

class Order(Base):
    __tablename__ = 'order'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    user_tg:Mapped[BigInteger] = mapped_column(BigInteger)
    addres:Mapped[str] = mapped_column(String)
    status:Mapped[str] = mapped_column(String)#todo choices
    delivered:Mapped[bool] = mapped_column(Boolean)
    price:Mapped[float] = mapped_column(Float)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
