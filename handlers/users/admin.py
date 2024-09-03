from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database.orm import ProductsDao, CategoriesDao
from filters.isAdmin import IsAdmin

admin_router = Router()

admin_commands = [
    KeyboardButton(text="Добавить категорию"),
    KeyboardButton(text="Добавить товар")
]

admin_markup = ReplyKeyboardMarkup(
    keyboard=[admin_commands],
    resize_keyboard=True
)

# Админская команда
@admin_router.message(Command(commands='admin'),IsAdmin())
async def admin_panel(message: types.Message):
    await message.answer("Добро пожаловать в админ-панель. Выберите действие:", reply_markup=admin_markup)

# Состояния для создания категории
class CategoryState(StatesGroup):
    input_name = State()

# Состояния для создания товара
class ProductState(StatesGroup):
    input_name = State()
    input_price = State()
    input_category = State()

# Добавление категории
@admin_router.message(F.text == 'Добавить категорию',IsAdmin())
async def add_category(message: types.Message, state: FSMContext):
    await state.set_state(CategoryState.input_name)
    await message.answer("Введите название новой категории:")

@admin_router.message(StateFilter(CategoryState.input_name))
async def save_category(message: types.Message, state: FSMContext):
    category_name = message.text
    await CategoriesDao.add_item(name=category_name)
    await state.clear()
    await message.answer(f"Категория '{category_name}' успешно добавлена!", reply_markup=admin_markup)

# Добавление товара
@admin_router.message(F.text == 'Добавить товар', IsAdmin())
async def add_product(message: types.Message, state: FSMContext):
    await state.set_state(ProductState.input_name)
    await message.answer("Введите название товара:")

@admin_router.message(StateFilter(ProductState.input_name))
async def input_product_name(message: types.Message, state: FSMContext):
    await state.update_data(product_name=message.text)
    await state.set_state(ProductState.input_price)
    await message.answer("Введите цену товара:")

@admin_router.message(StateFilter(ProductState.input_price))
async def input_product_price(message: types.Message, state: FSMContext):
    await state.update_data(product_price=message.text)
    await state.set_state(ProductState.input_category)
    categories = await CategoriesDao.find_all()
    categories_markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=category.name) for category in categories]],
        resize_keyboard=True
    )
    await message.answer("Выберите категорию товара:", reply_markup=categories_markup)

@admin_router.message(StateFilter(ProductState.input_category))
async def save_product(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    category_name = message.text
    category = await CategoriesDao.get_by(name=category_name)
    if category:
        await ProductsDao.add_item(
            name=user_data['product_name'],
            price=int(user_data['product_price']),
            category_id=category.id
        )
        await message.answer(f"Товар '{user_data['product_name']}' успешно добавлен в категорию '{category_name}'!", reply_markup=admin_markup)
    else:
        await message.answer("Категория не найдена. Попробуйте еще раз.")
    await state.clear()

