from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.types import MediaGroup

from create_bot import dp, bot
from messagePattern import replyPatterns, getCategoryInfo, getSubCategoryInfo, getClothInfo
from keyboard import clientKbDict, getSubCategoryKb
from keyboard import category as categoryList
from handlers.admin import adminId
from DatabaseHandler import getClothesList, getNumberOfClothes, deleteCloth as delFromBase
from LoggerHandler import ClientLogger, InitLogger

usedCommands = ['/start', '/help']

subCategories = ['Кроссовки', 'Кеды', 'Тапки', 'Худи', 'Свитшот', 'Флиска', 'T-shirt', 'Майка', 'Куртка', 'Пальто',
                 'Бомбер', 'Спортивные', 'Обычные']


class FSMClient(StatesGroup):
    defualtClient = State()
    categorySelect = State()
    subCategorySelect = State()
    showClothes = State()


# @dp.message_handler(Text(equals='информация', ignore_case=True))
async def info(message: types.Message):
    await bot.send_message(message.chat.id, 'Главный - @biruytskovskynf\n'
                                            'Если заметили некорректную работу бота, пишите - @vcdddk')


# @dp.callback_query_handler(text=['back','backToCat'],state='*')
async def backCallback(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'backToCat':
        await callback.message.edit_text(text=getCategoryInfo() + '\nВыберите категорию',
                                         reply_markup=clientKbDict['main'])
        await FSMClient.categorySelect.set()
    else:
        await back(callback.message, state)
    await callback.answer()


# @dp.message_handler(Text(equals='Назад', ignore_case=True),state='*')
async def back(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Возвращаюсь...', reply_markup=types.ReplyKeyboardRemove())
    if await state.get_state() == "FSMClient:showClothes":
        await bot.send_message(message.chat.id,
                               text=getCategoryInfo() + '\nВыберите категорию',
                               reply_markup=clientKbDict['main'])
        await FSMClient.categorySelect.set()
    else:
        await state.finish()
        await start(message)


# @dp.message_handler(commands=['start','help'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id,
                           text='Привет, это бот-каталог вещей магазина SecondRoom',
                           reply_markup=clientKbDict['start'])


# @dp.message_handler(Text(equals='каталог', ignore_case=True))
async def catalogEvent(message: types.Message):
    await FSMClient.categorySelect.set()
    await bot.send_message(message.chat.id, 'Открываю каталог', reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.chat.id, getCategoryInfo() + '\nВыберите категорию',
                           reply_markup=clientKbDict['main'])


# @dp.callback_query_handler(text=['Обувь','Верх','Низ'], state=FSMClient.categorySelect)
async def subcategorySelect(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as show:
        show['category'] = callback.data
    try:
        await callback.message.edit_text(text=getSubCategoryInfo(callback.data) + '\nВыберите подкатегорию',
                                         reply_markup=getSubCategoryKb(callback.data))
    except Exception as e:
        print(e, callback)

    await FSMClient.next()


# @dp.callback_query_handler(text=subCategories, state=FSMClient.subCategorySelect)
async def showClothes(callback: types.CallbackQuery, state: FSMContext, returned=False):
    await callback.answer()
    if not returned:
        async with state.proxy() as show:
            if callback.data not in categoryList[show['category']]:
                return
            else:
                show['subCategory'] = callback.data
    flipper = ['<<', 'Назад', '>>']
    flipperBut = (types.KeyboardButton(text) for text in flipper)
    flipperKb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    flipperKb.add(*flipperBut)
    # flipperKb.add(types.KeyboardButton('Написать владельцу'))
    if callback.from_user.id in adminId.keys():
        flipperKb.add(types.KeyboardButton('Удалить'))
    async with state.proxy() as show:
        show['clothes']: dict = dict(getClothesList([show['category'], show['subCategory']]))
        if show['clothes'] != {}:
            await bot.send_message(callback.message.chat.id, 'Вывод вещей по выбранной категории',
                                   reply_markup=flipperKb)
            cloth = list(show['clothes'].values())[0]
            show['currentCloth'] = 0
            show['currentClothId'] = list(show['clothes'].keys())[show['currentCloth']]
            show['countOfCloths'] = getNumberOfClothes([show['category'], show['subCategory']])
            show['currentClothMessages'] = list(await bot.send_media_group(callback.message.chat.id,
                                                                           media=await createMediaGroup(cloth,
                                                                                                        show[
                                                                                                            'currentCloth'] + 1,
                                                                                                        show[
                                                                                                            'countOfCloths'])))
            await FSMClient.next()
        else:
            ClientLogger.error(f'Не найдено вещей в категории {show["subCategory"]}')


# @dp.message_handler(Text(equals=['<<', '>>']), state=FSMClient.showClothes)
async def getAnother(message: types.Message, state: FSMContext, afterDelete=False):
    async with state.proxy() as show:
        current = show['currentCloth']
        for msg in show['currentClothMessages']:
            await msg.delete()
        if message.text == '<<':
            show['currentCloth'] = await checkIter(current - 1, show['countOfCloths'])
        elif message.text == '>>':
            show['currentCloth'] = await checkIter(current + 1, show['countOfCloths'])
        await sendCurrentCloth(message, show)
        # print(show['currentClothMessages'])


async def checkIter(current, total):
    if current < 0:
        return total - 1
    elif current == total:
        return 0
    else:
        return current


# @dp.message_handler(IDFilter(adminId), Text(equals='удалить', ignore_case=True), state=FSMClient.showClothes)
async def deleteCloth(message: types.Message, state: FSMContext):
    async with state.proxy() as show:
        pathToDelete = [show['category'], show['subCategory'], show['currentClothId']]
        delFromBase(pathToDelete)
        show['clothes']: dict = dict(getClothesList([show['category'], show['subCategory']]))
        if show['countOfCloths'] == 1:
            await bot.send_message(
                chat_id=message.chat.id,
                text=getSubCategoryInfo(show['category']) + '\nВыберите подкатегорию',
                reply_markup=getSubCategoryKb(show['category'])
            )
            await FSMClient.previous()
            return
        else:
            show['countOfCloths'] -= 1
            if show['currentCloth'] != 0:
                show['currentCloth'] -= 1
            await sendCurrentCloth(message, show)


async def sendCurrentCloth(message, show):
    cloth = list(show['clothes'].values())[show['currentCloth']]
    show['currentClothId'] = list(show['clothes'].keys())[show['currentCloth']]
    show['currentClothMessages'] = \
        list(await bot.send_media_group(message.chat.id,
                                        media=await createMediaGroup(cloth, show['currentCloth'] + 1,
                                                                     show['countOfCloths'])))


async def createMediaGroup(cloth, current, total):
    media = MediaGroup()
    for i in range(len(cloth['photo'])):
        media.attach_photo(
            types.InputMediaPhoto(cloth['photo'][i], caption=getClothInfo(cloth, current, total) if i == 0 else ''))
    return media


# @dp.message_handler(lambda message: message not in usedCommands)
async def default(message: types.Message):
    await bot.send_message(message.chat.id, replyPatterns['toStart'])


def registerHandlers():
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(catalogEvent, Text(equals='каталог', ignore_case=True))
    dp.register_message_handler(info, Text(equals='информация', ignore_case=True))
    dp.register_message_handler(back, Text(equals='Назад', ignore_case=True), state='*')
    dp.register_callback_query_handler(backCallback, text=['back', 'backToCat'], state='*')
    dp.register_message_handler(deleteCloth, IDFilter(adminId), Text(equals='удалить', ignore_case=True),
                                state=FSMClient.showClothes)
    dp.register_callback_query_handler(subcategorySelect, text=['Обувь', 'Верх', 'Низ'], state=FSMClient.categorySelect)
    dp.register_callback_query_handler(showClothes, state=FSMClient.subCategorySelect)
    dp.register_message_handler(getAnother, Text(equals=['<<', '>>']), state=FSMClient.showClothes)
    dp.register_message_handler(default, lambda message: message not in usedCommands)
    InitLogger.info('client handlers registered')


def registerHandlersDebug():
    dp.register_message_handler(start, commands=['start', 'help'], user_id=adminId.keys())
    dp.register_message_handler(catalogEvent, Text(equals='каталог', ignore_case=True), user_id=adminId.keys())
    dp.register_message_handler(info, Text(equals='информация', ignore_case=True), user_id=adminId.keys())
    dp.register_message_handler(back, Text(equals='Назад', ignore_case=True), state='*', user_id=adminId.keys())
    dp.register_callback_query_handler(backCallback, text=['back', 'backToCat'], state='*', user_id=adminId.keys())
    dp.register_message_handler(deleteCloth, IDFilter(adminId), Text(equals='удалить', ignore_case=True),
                                state=FSMClient.showClothes, user_id=adminId.keys())
    dp.register_callback_query_handler(subcategorySelect, text=['Обувь', 'Верх', 'Низ'], state=FSMClient.categorySelect,
                                       user_id=adminId.keys())
    dp.register_callback_query_handler(showClothes, state=FSMClient.subCategorySelect, user_id=adminId.keys())
    dp.register_message_handler(getAnother, Text(equals=['<<', '>>']), state=FSMClient.showClothes,
                                user_id=adminId.keys())
    dp.register_message_handler(default, lambda message: message not in usedCommands, user_id=adminId.keys())
    InitLogger.info('debug client handlers registered')
