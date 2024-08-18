from imghdr import tests

from sqlalchemy import Column, Integer, BigInteger, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from database.database import Base


class Hotelstest(Base):
    __tablename__ = 'hotelstest'
    id:int = Column(Integer, primary_key=True)
    count:int = Column(Integer)

class Category(Base):
    __tablename__ = 'category'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String)

class User(Base):
    __tablename__ = 'user'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id:Mapped[BigInteger] = mapped_column(BigInteger)

class Product(Base):
    __tablename__ = 'product'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String)
    price:Mapped[float] = mapped_column(Float)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))