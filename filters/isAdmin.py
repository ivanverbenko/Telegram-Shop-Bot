from aiogram.filters import Filter
from aiogram.types import Message


from config import ADMINS


class IsAdmin(Filter):

    async def __call__(self, message: Message):
        return message.from_user.id in ADMINS
