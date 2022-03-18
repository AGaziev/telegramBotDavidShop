from create_bot import bot, dp, fsm
from keyboard import adminKbDict, otherKbDict, category
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from DatabaseHandler import DBcontroller

adminId = {1256578670: 'David',
           292667494: 'Alan'}


class FSMAdmin(StatesGroup):
    category = State()
    subCategory = State()
    brand = State()
    name = State()
    price = State()
    condition = State()
    photo = State()
    GroupStates = {
        'addCloth': [category, subCategory, brand, name, price, photo]
    }


# @dp.message_handler(state=FSMAdmin.GroupStates['addCloth'], commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state=FSMAdmin.GroupStates['addCloth'])
async def cancelAdd(message: types.Message, state: FSMContext):
    if message.from_user.id in adminId.keys():
        print('cancel admin panel')
    await message.reply('Возвращаюсь...')
    await state.finish()


# @dp.message_handler(commands=['admin'], state=None)
async def admStart(message: types.Message):
    if message.from_user.id in adminId.keys():
        print(adminId[message.from_user.id], 'on admin panel')
        await bot.send_message(message.chat.id, 'Успешный вход на панель админа',
                               reply_markup=adminKbDict['adminPanelInline'])
    else:
        await message.reply('Недостаточно прав')


# @dp.callback_query_handler(text='addCloth')
async def startAdding(call: types.CallbackQuery):
    await call.message.edit_text('Добавление вещи...')
    catKb = otherKbDict['main']
    catKb.one_time_keyboard = True
    await bot.send_message(call.from_user.id, 'Выберите категорию', reply_markup=otherKbDict['main'])
    del catKb
    await call.answer('start adding new cloth', show_alert=False)
    await FSMAdmin.category.set()


# @dp.message_handler(Text(equals=category.keys(), ignore_case=False), state=FSMAdminAdd.category)
async def chooseSubCategory(message: types.Message, state: FSMContext):
    # await message.delete_reply_markup()
    async with state.proxy() as data:
        data['category'] = message.text
    await FSMAdmin.next()
    subCatKb = otherKbDict[message.text]
    subCatKb.one_time_keyboard = True
    await bot.send_message(message.chat.id, 'Выберите подкатегорию',
                           reply_markup=subCatKb)
    del subCatKb


# @dp.message_handler(state=FSMAdminAdd.subCategory)
async def chooseBrand(message: types.Message, state: FSMContext):
    # await message.delete_reply_markup()
    async with state.proxy() as data:
        data['subCategory'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, 'Напишите бренд (\'-\' для пропуска)')


# @dp.message_handler(state=FSMAdminAdd.brand)
async def chooseName(message: types.Message, state: FSMContext):
    if message.text != '-':
        async with state.proxy() as data:
            data['brand'] = message.text
    else:
        async with state.proxy() as data:
            data['brand'] = None
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, 'Напишите название (\'-\' для пропуска)')


# @dp.message_handler(state=FSMAdminAdd.name)
async def choosePrice(message: types.Message, state: FSMContext):
    if message.text != '-':
        async with state.proxy() as data:
            data['name'] = message.text
    else:
        async with state.proxy() as data:
            data['name'] = None
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, 'Напишите цену (\'-\' для пропуска)')


# @dp.message_handler(state=FSMAdminAdd.price)
async def chooseCondition(message: types.Message, state: FSMContext):
    if message.text != '-':
        async with state.proxy() as data:
            data['price'] = float(message.text)
    else:
        async with state.proxy() as data:
            data['price'] = 'Бесплатно'
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, 'Выберите состояние',
                           reply_markup=adminKbDict['condition'])


# @dp.message_handler(state=FSMAdminAdd.condition)
async def choosePhoto(message: types.Message, state: FSMContext):
    # await message.delete_reply_markup()
    async with state.proxy() as data:
        data['condition'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, 'Загрузите фото')


# @dp.message_handler(content_types = ['photo'], state=FSMAdminAdd.photo)
async def endAddingCloth(message: types.Message, state: FSMContext):
    if message.text != '-':
        async with state.proxy() as data:
            data['photo'] = []
            for photo in message.photo[3::4]:
                data['photo'].append(photo.file_id)
    async with state.proxy() as data:
        DBcontroller.addCloth(data)
    await state.finish()
    await admStart(message)


def register_handlers():
    # cancel state handlers
    dp.register_message_handler(cancelAdd, commands='отмена', state=FSMAdmin.GroupStates['addCloth'])
    dp.register_message_handler(cancelAdd, Text(equals='отмена', ignore_case=True),
                                state=FSMAdmin.GroupStates['addCloth'])
    # admin panel handler
    dp.register_message_handler(admStart, commands=['admin'])
    # add cloth handlers
    dp.register_callback_query_handler(startAdding, text='addCloth')
    dp.register_message_handler(chooseSubCategory, Text(equals=category.keys(), ignore_case=False),
                                state=FSMAdmin.category)
    dp.register_message_handler(chooseBrand, state=FSMAdmin.subCategory)
    dp.register_message_handler(chooseName, state=FSMAdmin.brand)
    dp.register_message_handler(choosePrice, state=FSMAdmin.name)
    dp.register_message_handler(chooseCondition, state=FSMAdmin.price)
    dp.register_message_handler(choosePhoto, state=FSMAdmin.condition)
    dp.register_message_handler(endAddingCloth, content_types=['photo'], state=FSMAdmin.photo)
    ###
    print('registered Admin handlers')
