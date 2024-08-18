from aiogram.filters import Filter
from aiogram.types import Message


from config import ADMINS


class IsUser(Filter):

    async def check(self, message: Message):
        return message.from_user.id not in ADMINS
