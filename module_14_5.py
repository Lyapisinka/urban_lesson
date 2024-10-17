import sqlite3

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils import executor
import logging
from crud_functions2 import initiate_db, get_all_products, add_user, is_included

API_TOKEN = '1957811194:AAF2vBDuGO9LVbJPyva_r3l2H2MszR0VBQg'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())

# Создаем главную клавиатуру с нужными кнопками
main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_keyboard.add(KeyboardButton("Купить"))
main_menu_keyboard.add(KeyboardButton("Рассчитать"), KeyboardButton("Информация"))
main_menu_keyboard.add(KeyboardButton("Регистрация"))
inline_menu = InlineKeyboardMarkup()
inline_buttons = [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
                  InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
inline_menu.add(*inline_buttons)

# Создаем Inline клавиатуру
inline_keyboard = InlineKeyboardMarkup(row_width=4)
inline_buttons = [InlineKeyboardButton(f"Product{i+1}", callback_data="product_buying") for i in range(4)]
inline_keyboard.add(*inline_buttons)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Выберите действие:", reply_markup=main_menu_keyboard)


@dp.message_handler(lambda message: message.text == "Регистрация")
async def sign_up(message: types.Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text
    if is_included(username):
        await message.answer("Пользователь существует, введите другое имя")
        return

    await state.update_data(username=username)
    await message.answer("Введите свой email:")
    await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)

    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        user_data = await state.get_data()
        add_user(user_data['username'], user_data['email'], age)

        await message.answer("Регистрация завершена!", reply_markup=main_menu_keyboard)
        await state.finish()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число для возраста.")


@dp.message_handler(lambda message: message.text == "Информация")
async def get_info(message: types.Message):
    await message.answer(
        "Формула Миффлина-Сан Жеора:\nДля мужчин: 10 * вес + 6.25 * рост - 5 * возраст + 5\nДля женщин: 10 * вес + 6.25 * рост - 5 * возраст - 161")

@dp.message_handler(lambda message: message.text == "Купить")
async def get_buying_list(message: types.Message):
    products = get_all_products()

    # Вывод информации о продуктах с картинками
    for i, (title, description, price) in enumerate(products, start=1):
        try:
            with open(f'{i}.jpg', 'rb') as f:  # Путь к картинке
                await message.answer_photo(f, f'Название: {title} | Описание: {description} | Цена: {price}')
        except FileNotFoundError:
            await message.answer(f'Изображение для продукта "{title}" не найдено.')

    # Вывод Inline меню
    await message.answer("Выберите продукт для покупки:", reply_markup=inline_keyboard)

@dp.callback_query_handler(lambda call: call.data == "product_buying")
async def send_confirm_message(call: CallbackQuery):
    await call.answer()  # Закрыть уведомление о нажатии
    await call.message.answer("Вы успешно приобрели продукт!")

@dp.message_handler(Text(equals='Рассчитать', ignore_case=True))
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост (в см):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес (в кг):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    try:
        # Попытка обновления данных о весе
        weight = int(message.text)
        await state.update_data(weight=weight)

        # Получение других данных из состояния
        data = await state.get_data()

        # Рассчитываем BMR
        bmr = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5

        # Ответ пользователю с результатами и возвращение к главному меню
        await message.answer(f'Ваша базовая норма калорий: {bmr} ккал в день.', reply_markup=main_menu_keyboard)

        # Сбрасываем состояние
        await state.finish()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число для веса.")


def add_sample_products():
    conn = sqlite3.connect('product.db')
    cursor = conn.cursor()

    sample_products = [('Продукт 1', 'Описание продукта 1', 100), ('Продукт 2', 'Описание продукта 2', 200),
        ('Продукт 3', 'Описание продукта 3', 300), ('Продукт 4', 'Описание продукта 4', 400), ]

    cursor.executemany('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', sample_products)

    conn.commit()
    conn.close()





if __name__ == '__main__':
    initiate_db()
    #add_sample_products()
    executor.start_polling(dp, skip_updates=True)
