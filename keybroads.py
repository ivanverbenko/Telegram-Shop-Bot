from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.orm import CategoriesDao, ProductsDao

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

async def products(category_id: int):
    products = await ProductsDao.find_by(category_id=int(category_id))
    products_kb = InlineKeyboardBuilder()
    for product in products:
        products_kb.add(InlineKeyboardButton(text=product.name, callback_data=f'product_{product.id}'))
    return products_kb.adjust(2).as_markup()

async def product(id: int):
    product = await ProductsDao.get_by_id(id)
    product_kb = InlineKeyboardBuilder()
    product_kb.add(InlineKeyboardButton(text=f"заказать товар", callback_data=f'order_{product.id}'))
    return product_kb.as_markup()

def confirmation_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data='confirm_yes'),
                InlineKeyboardButton(text="Нет", callback_data='confirm_no')
            ]
        ]
    )
    return keyboard