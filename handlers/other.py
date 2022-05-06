from create_bot import bot, dp
from aiogram import Dispatcher
from LoggerHandler import InitLogger


def register_handlers():
    InitLogger.info('other handlers registered')
