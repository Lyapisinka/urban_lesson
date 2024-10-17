from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import asyncio

API_TOKEN = ''


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')]
keyboard.add(*buttons)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Выберите действие:', reply_markup=keyboard)


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
    await state.update_data(weight=int(message.text))
    data = await state.get_data()

    bmr = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5

    await message.answer(f'Ваша базовая норма калорий: {bmr} ккал в день.')

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)