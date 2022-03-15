from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import botConfigure
# конфиг бота

try:
    bot = Bot(token=configure.config['token'])
    dp = Dispatcher(bot)
except:
    print('Произошла ошибка при авторизации токена')

fsm = MemoryStorage
