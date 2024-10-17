from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils import executor
import logging

API_TOKEN = '1957811194:AAF2vBDuGO9LVbJPyva_r3l2H2MszR0VBQg'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())

# Создаем главную клавиатуру с нужными кнопками
main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_keyboard.add(KeyboardButton("Купить"))
main_menu_keyboard.add(KeyboardButton("Рассчитать"), KeyboardButton("Информация"))

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


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Выберите действие:", reply_markup=main_menu_keyboard)


@dp.message_handler(lambda message: message.text == "Информация")
async def get_info(message: types.Message):
    await message.answer(
        "Формула Миффлина-Сан Жеора:\nДля мужчин: 10 * вес + 6.25 * рост - 5 * возраст + 5\nДля женщин: 10 * вес + 6.25 * рост - 5 * возраст - 161")

@dp.message_handler(lambda message: message.text == "Купить")
async def get_buying_list(message: types.Message):
    # Вывод информации о продуктах с картинками
    for i in range(1, 5):
        with open(f'{i}.jpg', 'rb') as f:# Путь к картинке

            await message.answer_photo(f, f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}')

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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
