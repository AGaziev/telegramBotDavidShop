from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from keyboard import clientKbDict
from messagePattern import replyPatterns, getCategoryInfo, getSubCategoryInfo

usedCommands = ['/start', '/help']


class FSMClient(StatesGroup):
    CategorySelect = State()
    SubCategorySelect = State()
    ShowClothes = State()


# @dp.message_handler(Text(equals='информация', ignore_case=True))
async def info(message: types.Message):
    await bot.send_message(message.chat.id, 'Информации нет')


# @dp.message_handler(commands=['start','help'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id,
                           text='''Привет эта я давит пипец она наверно меня не слышит это я давит седня какое \
а какое седня кароче апрель воскресенье две тыщи тринадцатый пака хихихи''',
                           reply_markup=clientKbDict['start'])


# @dp.message_handler(Text(equals='каталог', ignore_case=True))
async def catalogEvent(message: types.Message):
    await FSMClient.CategorySelect.set()
    await bot.send_message(message.chat.id, getCategoryInfo() + '\nВыберите подкатегорию',
                           reply_markup=clientKbDict['main'])


# @dp.callback_query_handler(text=['Обувь','Верх','Низ'], state=FSMClient.CategorySelect)
async def subcategorySelect(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as show:
        show['category'] = callback.data
    await callback.message.edit_text(text=getSubCategoryInfo(callback.data), reply_markup=clientKbDict[callback.data])


# @dp.message_handler(lambda message: message not in usedCommands)
async def default(message: types.Message):
    await bot.send_message(message.chat.id, replyPatterns['toStart'])


def register_handlers():
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(catalogEvent, Text(equals='каталог', ignore_case=True))
    dp.register_callback_query_handler(subcategorySelect, text=['Обувь', 'Верх', 'Низ'], state=FSMClient.CategorySelect)
    dp.register_message_handler(default, lambda message: message not in usedCommands)
    print('registered Client handlers')
