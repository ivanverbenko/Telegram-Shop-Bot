from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

from keybroads import categories



catalog_button = KeyboardButton(text="Каталог")
cart_button = KeyboardButton(text="Корзина")
delivery_status_button = KeyboardButton(text="Статус доставки")

settings = '⚙️ Настройка каталога'
orders = '🚚 Заказы'
questions = '❓ Вопросы'

# @dp.message(IsAdmin(), commands='menu')
# async def admin_menu(message: Message):
#     markup = ReplyKeyboardMarkup(selective=True)
#     markup.add(settings)
#     markup.add(questions, orders)
#
#     await message.answer('Меню', reply_markup=markup)
#
#
# @dp.message(IsUser(), commands='menu')
# async def user_menu(message: Message):
#     markup = ReplyKeyboardMarkup(selective=True)
#     markup.add(catalog)
#     markup.add(cart)
#     markup.add(delivery_status)
#
#     await message.answer('Меню', reply_markup=markup)
router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    user_button = KeyboardButton(text="Каталог")
    admin_button = KeyboardButton(text='admin_message')

    # Создание разметки клавиатуры
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [user_button, admin_button]
        ],
        resize_keyboard=True
    )

    await message.answer('''Привет! 👋

🤖 Я бот-магазин по подаже товаров любой категории.

🛍️ Чтобы перейти в каталог и выбрать приглянувшиеся 
товары возпользуйтесь командой /catalog.

❓ Возникли вопросы? Не проблема! Команда /sos поможет 
связаться с админами, которые постараются как можно быстрее откликнуться.
    ''', reply_markup=markup)

@router.message(F.text=='Каталог')
async def catalog(message: types.Message):
    await message.answer("Выберите вариант из каталога", reply_markup= await categories())

@router.callback_query(F.data.startswith('category_'))
async def category_selected(callback: CallbackQuery):
    category_id = callback.data
    await callback.message.answer(f"Выбрана категория")

@router.message(Command(commands='menu'))
async def user_menu(message: types.Message):
    # Создание разметки клавиатуры
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [catalog_button, cart_button],
            [delivery_status_button]
        ],
        resize_keyboard=True,  # Адаптация клавиатуры под размер кнопок
        one_time_keyboard=True  # Скрытие клавиатуры после выбора
    )

    # Отправка сообщения с клавиатурой
    await message.answer('Меню', reply_markup=markup)
