from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboard import clientKbDict
from messagePattern import replyPatterns

usedCommands = ['/start', '/help']


# @dp.message_handler(commands=['start','help'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id,
                           '''Привет эта я давит пипец она наверно меня не слышит это я давит седня какое 
                           а какое седня кароче апрель воскресенье две тыщи тринадцатый пака хихихи''',
                           reply_markup=clientKbDict['start'])


# @dp.message_handler(lambda message: message not in usedCommands)
async def default(message: types.Message):
    await bot.send_message(message.chat.id, replyPatterns['toStart'])


def register_handlers():
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(default, lambda message: message not in usedCommands)
    print('registered Client handlers')
