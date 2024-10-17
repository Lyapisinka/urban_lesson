from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncio

API_TOKEN = ''  # Замените на ваш токен

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Обработчик для команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет! Я ваш бот, и я готов помочь вам!')

# Обработчик для всех входящих сообщений
@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer('Вы написали: ' + message.text)

# Запуск бота


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

