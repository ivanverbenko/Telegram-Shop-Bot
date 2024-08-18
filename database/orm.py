from sqlalchemy import select

from database.database import async_session_maker
from database.models import Hotelstest, Category


class BaseDao:
    model = None
    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query=select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

class CategoriesDao(BaseDao):
    model = Category