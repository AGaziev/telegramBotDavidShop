from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboard import kb_client
import random


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, message.text, reply_markup=kb_client)


@dp.message_handler()
async def checkLoh(message: types.Message):
    lohPercent = random.randint(0, 100)
    if message.text == 'Проверка на лоха':
        await bot.send_message(message.chat.id, f'{message.chat.first_name} на {lohPercent}% лох')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(checkLoh)
