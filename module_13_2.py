from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

# Вставьте сюда ваш токен от BotFather
API_TOKEN = ''

# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Обработчик для команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.reply('Привет! Я бот помогающий твоему здоровью.')  # Отвечаем в чате


# Обработчик для всех других сообщений
@dp.message_handler()
async def all_messages(message: types.Message):
    print('Введите команду /start, чтобы начать общение.')
    await message.reply('Введите команду /start, чтобы начать общение.')  # Отвечаем в чате


if __name__ == '__main__':
    import logging

    # Настраиваем ведение журнала
    logging.basicConfig(level=logging.INFO)

    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)