from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, MediaGroup

from create_bot import dp, bot
from keyboard import clientKbDict
from messagePattern import replyPatterns, getCategoryInfo, getSubCategoryInfo, getClothInfo
from keyboard import category as categoryList
from handlers.admin import adminId
from DatabaseHandler import getClothesList, getNumberOfClothes

usedCommands = ['/start', '/help']


class FSMClient(StatesGroup):
    defualtClient = State()
    categorySelect = State()
    subCategorySelect = State()
    showClothes = State()


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
    await FSMClient.categorySelect.set()
    await bot.send_message(message.chat.id, getCategoryInfo() + '\nВыберите подкатегорию',
                           reply_markup=clientKbDict['main'])


# @dp.callback_query_handler(text=['Обувь','Верх','Низ'], state=FSMClient.categorySelect)
async def subcategorySelect(callback: types.CallbackQuery, state: FSMContext, returned=False):
    await callback.answer()
    await FSMClient.next()
    if not returned:
        async with state.proxy() as show:
            show['category'] = callback.data
    await callback.message.edit_text(text=getSubCategoryInfo(callback.data), reply_markup=clientKbDict[callback.data])


# @dp.callback_query_handler(state=FSMClient.subCategorySelect)
async def showClothes(callback: types.CallbackQuery, state: FSMContext, returned=False):
    await callback.answer()
    if not returned:
        async with state.proxy() as show:
            if callback.data not in categoryList[show['category']]:
                return
            else:
                show['subCategory'] = callback.data
    flipper = [
        ('>>', 'next'),
        ('Назад', 'back')
    ]
    flipperBut = (types.InlineKeyboardButton(text, callback_data=data) for text, data in flipper)
    flipperKb = types.InlineKeyboardMarkup()
    flipperKb.add(*flipperBut)
    if callback.from_user.id in adminId.keys():
        flipperKb.add(types.InlineKeyboardButton('Удалить', callback_data='delete'))
    async with state.proxy() as show:
        show['clothes']: dict = dict(getClothesList([show['category'], show['subCategory']]))
        if show['clothes']:
            cloth = list(show['clothes'].values())[0]
            show['currentCloth'] = 0
            show['currentClothId'] = list(show['clothes'].keys())[show['currentCloth']]
            show['countOfCloths'] = getNumberOfClothes([show['category'], show['subCategory']])
            print(cloth, show['currentClothId'], show['countOfCloths'])
            messages = await bot.send_media_group(callback.message.chat.id,
                                                  media=await createMediaGroup(cloth, show['countOfCloths']))
            await FSMClient.next()
        else:
            await callback.message.edit_text()


async def createMediaGroup(cloth, count):
    media = MediaGroup()
    for i in range(count):
        media.attach_photo(types.InputMediaPhoto(cloth['photo'][i], caption=getClothInfo(cloth) if i == 0 else ''))
    return media


@dp.callback_query_handler(state=FSMClient.showClothes, text=['next', 'previous'])
async def clothesShower(callback: CallbackQuery, state: FSMContext):
    tempKb = clientKbDict['flip']
    if callback.from_user.id in adminId.keys():
        tempKb.add(types.InlineKeyboardButton('Удалить', callback_data='delete'))
    async with state.proxy() as show:
        pass


# @dp.message_handler(lambda message: message not in usedCommands)
async def default(message: types.Message):
    await bot.send_message(message.chat.id, replyPatterns['toStart'])


def register_handlers():
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(catalogEvent, Text(equals='каталог', ignore_case=True))
    dp.register_callback_query_handler(subcategorySelect, text=['Обувь', 'Верх', 'Низ'], state=FSMClient.categorySelect)
    dp.register_callback_query_handler(showClothes, state=FSMClient.subCategorySelect)
    dp.register_message_handler(default, lambda message: message not in usedCommands)
    print('registered Client handlers')
