from LoggerHandler import InitLogger
from create_bot import dp, bot

from aiogram import types
from aiogram.dispatcher.filters import Text

# @dp.message_handler(Text(equals='каталог', ignore_case=True))
async def technicalPause(message:types.Message):
    await bot.send_message(message.chat.id, 'Технический перерыв')

def registerHandlers():
    dp.register_message_handler(technicalPause, Text(equals='Каталог', ignore_case=True))
    InitLogger.info('other handlers registered')
