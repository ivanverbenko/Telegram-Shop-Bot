from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.database import async_session_maker
from database.models import Category, Product, Order


class BaseDao:
    model = None
    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query=select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_by_id(cls, id):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == id)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def get_by(cls, **kwargs):
        """
        Метод для гибкого поиска одного объекта по переданным условиям.
        Пример использования:
        await ProductsDao.find_by(category_id=1, name='Product Name')
        """
        async with async_session_maker() as session:
            # Формируем условие на основе переданных kwargs
            conditions = [getattr(cls.model, key) == value for key, value in kwargs.items()]
            query = select(cls.model).where(*conditions)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def find_by(cls, **kwargs):
        async with async_session_maker() as session:
            conditions = [getattr(cls.model, key) == value for key, value in kwargs.items()]
            query = select(cls.model).where(*conditions)
            result = await session.execute(query)
            return result.scalars().all()
    @classmethod
    async def add_item(cls, **kwargs):
        async with async_session_maker() as session:
            async with session.begin():
                print('go')
                item = cls.model(**kwargs)
                print(item)
                session.add(item)
                print('added')
                await session.commit()


class CategoriesDao(BaseDao):
    model = Category

class ProductsDao(BaseDao):
    model = Product


class OrdersDao(BaseDao):
    model = Order