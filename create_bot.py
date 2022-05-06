from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from LoggerHandler import InitLogger
import os

fsm = MemoryStorage()

try:
    bot = Bot(token=os.getenv("botToken"),)
    dp = Dispatcher(bot, storage=fsm)
except:
    InitLogger.critical('Произошла ошибка при авторизации токена')
    print('Произошла ошибка при авторизации токена')
