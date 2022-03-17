from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import botConfigure
# конфиг бота

fsm = MemoryStorage()

try:
    bot = Bot(token=botConfigure.config['token'])
    dp = Dispatcher(bot,storage=fsm)
except:
    print('Произошла ошибка при авторизации токена')

