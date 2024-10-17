from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor


API_TOKEN = ''

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Создание клавиатуры для главного меню
main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_buttons = [KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')]
main_menu_keyboard.add(*main_menu_buttons)

inline_menu = InlineKeyboardMarkup()
inline_buttons = [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
    InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
inline_menu.add(*inline_buttons)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Выберите действие:', reply_markup=main_menu_keyboard)


@dp.message_handler(lambda message: message.text.lower() == 'рассчитать')
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=inline_menu)


@dp.callback_query_handler(lambda c: c.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer(
        "Формула Миффлина-Сан Жеора:\nДля мужчин: 10 * вес + 6.25 * рост - 5 * возраст + 5\nДля женщин: 10 * вес + 6.25 * рост - 5 * возраст - 161")
    await call.answer()


@dp.callback_query_handler(lambda c: c.data == 'calories')
async def set_age(call: types.CallbackQuery):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


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