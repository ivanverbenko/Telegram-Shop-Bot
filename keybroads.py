from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.orm import CategoriesDao

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог')],
    [KeyboardButton(text='Контакты')]
])

async def categories():
    categories = await CategoriesDao.find_all()
    categories_cb = InlineKeyboardBuilder()
    for category in categories:
        categories_cb.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))
        print(str(category.id))
    return categories_cb.adjust(2).as_markup()

