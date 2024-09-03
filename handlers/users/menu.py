from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

from database.orm import ProductsDao, OrdersDao
from keybroads import categories, products, product, confirmation_keyboard, main

catalog_button = KeyboardButton(text="Каталог")
cart_button = KeyboardButton(text="Корзина")
delivery_status_button = KeyboardButton(text="Статус доставки")

settings = '⚙️ Настройка каталога'
orders = '🚚 Заказы'
questions = '❓ Вопросы'

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    user_button = KeyboardButton(text="Каталог")
    status_delivery = KeyboardButton(text='Статус доставки')

    markup = ReplyKeyboardMarkup(
        keyboard=[
            [user_button, status_delivery]
        ],
        resize_keyboard=True
    )

    await message.answer('''Привет! 👋

🤖 Я бот-магазин по подаже товаров любой категории.
    ''', reply_markup=markup)

@router.message(F.text=='Каталог')
async def catalog(message: types.Message):
    await message.answer("Выберите вариант из каталога", reply_markup= await categories())

@router.message(F.text == 'Статус доставки')
async def track_order(message: types.Message):
    orders = await OrdersDao.find_by(user_tg=message.from_user.id)
    for order in orders:
        delivered_status = "Доставлен" if order.delivered else "Не доставлен"
        await message.answer(
            f"Заказ #{order.id}:\n"
            f"Адрес: {order.addres}\n"
            f"Статус: {order.status}\n"
            f"Цена: {order.price}\n"
            f"Доставка: {delivered_status}"
        )

@router.callback_query(F.data.startswith('category_'))
async def category_selected(callback: CallbackQuery):
    category_id = callback.data.split('_')[-1]
    await callback.message.answer(f'Товары выбранной категории: ', reply_markup= await products(category_id))

@router.callback_query(F.data.startswith('product_'))
async def product_selected(callback: CallbackQuery):
    product_id = int(callback.data.split('_')[-1])
    product_obj = await ProductsDao.get_by_id(id=product_id)
    await callback.message.answer(f'Информация о товаре:\nТовар: {product_obj.name}\nЦена: {product_obj.price} ',
                                  reply_markup= await product(product_id))
@router.message(Command(commands='menu'))
async def user_menu(message: types.Message):
    # Создание разметки клавиатуры
    markup = main

    # Отправка сообщения с клавиатурой
    await message.answer('Меню', reply_markup=markup)

class CheckoutState(StatesGroup):
    input_name = State()
    input_address = State()
    confirm_order = State()

@router.message(StateFilter('*'), F.text == 'Отменить заказ')
async def cancel_order(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Оформление заказа отменено.")


@router.callback_query(F.data.startswith('order_'))
async def start_checkout(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split('_')[-1])
    await state.update_data(product_id=product_id)

    await state.set_state(CheckoutState.input_name)
    await callback.message.answer("Пожалуйста, введите ваше имя:")



@router.message(StateFilter(CheckoutState.input_name))
async def input_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CheckoutState.input_address)
    await message.answer("Пожалуйста, введите ваш адрес:")


@router.message(StateFilter(CheckoutState.input_address))
async def input_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(CheckoutState.confirm_order)
    user_data = await state.get_data()
    product_id = user_data.get('product_id')
    product_obj = await ProductsDao.get_by_id(id=product_id)

    confirmation_text = (
        f"Ваш заказ:\n"
        f"Товар: {product_obj.name}\n"
        f"Цена: {product_obj.price}\n"
        f"Имя: {user_data['name']}\n"
        f"Адрес: {user_data['address']}\n\n"
        "Пожалуйста, подтвердите ваш заказ, используя кнопки ниже."
    )

    await message.answer(
        text=confirmation_text,
        reply_markup=confirmation_keyboard()
    )


@router.callback_query(StateFilter(CheckoutState.confirm_order))
async def handle_confirmation(callback: CallbackQuery, state: FSMContext):
    markup=main
    if callback.data == 'confirm_yes':
        user_data = await state.get_data()
        product_id = user_data.get('product_id')
        product_obj = await ProductsDao.get_by_id(id=product_id)
        await OrdersDao.add_item(addres=user_data['address'],status='заказ оформлен',
                                 delivered=False, user_tg=callback.from_user.id, product_id=product_id,
                                 price = product_obj.price)
        await callback.message.answer(
            f"Ваш заказ на товар '{product_obj.name}'"
            f" подтвержден!\nИмя: {user_data['name']}\n"
            f"Адрес: {user_data['address']}\nСпасибо за покупку!",
            reply_markup=markup
        )
    elif callback.data == 'confirm_no':
        await callback.message.answer("Заказ отменен.",reply_markup=markup)

    await state.clear()
