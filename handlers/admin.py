﻿from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from create_bot import bot, dp
from keyboard import adminKbDict, getSubCategoryKbAdmin
from DatabaseHandler import DBcontroller, getAdmin, getCategories
from LoggerHandler import AdminLogger, InitLogger
from messagePattern import getClothInfoForChannel

import datetime

generalChannelId = -1001508153758


class FSMAdmin(StatesGroup):
    category = State()
    subCategory = State()
    brand = State()
    name = State()
    price = State()
    size = State()
    condition = State()
    photo = State()
    GroupStates = {
        'addCloth': [category, subCategory, brand, name, price, size, condition, photo]
    }


# @dp.message_handler(state=FSMAdmin.GroupStates['addCloth'], commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state=FSMAdmin.GroupStates['addCloth'])
async def cancelAdd(message: types.Message, state: FSMContext):
    if message.from_user.id in getAdmin().keys():
        AdminLogger.info(f'{message.chat.id} exit admin panel')
    await message.reply('Отмена')
    await state.finish()


# # @dp.message_handler(state=FSMAdmin.GroupStates['addCloth'], commands='назад')
# # @dp.message_handler(Text(equals='назад', ignore_case=True), state=FSMAdmin.GroupStates['addCloth'])
# async def cancelAdd(message: types.Message, state: FSMContext):
#     if message.from_user.id in adminId.keys():
#         print('to previous state state')
#     await message.reply('Возвращаюсь...')
#     await FSMAdmin.previous()

# @dp.message_handler(commands=['admin'], state=None)
async def admLogin(message: types.Message, logged=False):
    if message.from_user.id in getAdmin().keys():
        if not logged:
            AdminLogger.info(f'{getAdmin()[message.from_user.id]} entered admin panel')
        await bot.send_message(message.chat.id, 'Успешный вход на панель админа',
                               reply_markup=adminKbDict['adminPanelInline'])
    else:
        await message.reply('Недостаточно прав')


# @dp.callback_query_handler(text='addCloth')
async def startAdding(call: types.CallbackQuery):
    await call.message.edit_text('Добавление вещи...')
    AdminLogger.info(f'{getAdmin()[call.from_user.id]} started to add new Cloth')
    await bot.send_message(call.from_user.id, 'Выберите категорию', reply_markup=adminKbDict['main'])
    await call.answer('start adding new cloth', show_alert=False)
    await FSMAdmin.category.set()


# @dp.message_handler(Text(equals=category.keys(), ignore_case=False), state=FSMAdmin.category)
async def chooseSubCategory(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await FSMAdmin.next()
    subCatKb = getSubCategoryKbAdmin(message.text)
    subCatKb.one_time_keyboard = True
    await bot.send_message(message.chat.id, 'Выберите подкатегорию',
                           reply_markup=subCatKb)
    del subCatKb


# @dp.message_handler(state=FSMAdmin.subCategory)
async def chooseBrand(message: types.Message, state: FSMContext):
    # await message.delete_reply_markup()
    async with state.proxy() as data:
        data['subCategory'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, 'Напишите бренд (\'-\' для пропуска)', reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(state=FSMAdmin.brand)
async def chooseName(message: types.Message, state: FSMContext):
    if message.text != '-':
        async with state.proxy() as data:
            data['brand'] = message.text
    else:
        async with state.proxy() as data:
            data['brand'] = 'None'
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, 'Напишите название (\'-\' для пропуска)')


# @dp.message_handler(state=FSMAdmin.name)
async def choosePrice(message: types.Message, state: FSMContext):
    if message.text != '-':
        async with state.proxy() as data:
            data['name'] = message.text
    else:
        async with state.proxy() as data:
            data['name'] = 'None'
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, 'Напишите цену (\'-\' для пропуска)')


# @dp.message_handler(state=FSMAdmin.price)
async def chooseSize(message: types.Message, state: FSMContext):
    if message.text != '-':
        async with state.proxy() as data:
            data['price'] = message.text
    else:
        async with state.proxy() as data:
            data['price'] = 'None'
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, 'Напишите размер')


# @dp.message_handler(state=FSMAdmin.size)
async def chooseCondition(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, 'Выберите состояние',
                           reply_markup=adminKbDict['condition'])


# @dp.message_handler(state=FSMAdminAdd.condition)
async def choosePhoto(message: types.Message, state: FSMContext):
    # await message.delete_reply_markup()
    async with state.proxy() as data:
        data['condition'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, 'Загрузите фото', reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(content_types = ['photo','text], state=FSMAdmin.photo)
async def endAddingCloth(message: types.Message, state: FSMContext):
    if message.text != '-':
        async with state.proxy() as data:
            if 'photo' not in data:
                data['photo'] = []
            data['photo'].append(message.photo[0].file_id)
    kbAddPhoto = InlineKeyboardMarkup()
    kbAddPhoto.add(InlineKeyboardButton('Нет', callback_data='returnToAdmin'))
    await bot.send_message(message.chat.id, 'Фото добавлено. Ещё фото?', reply_markup=kbAddPhoto)


# @dp.callback_query_handler(state=FSMAdmin.photo,text='returnToAdmin')
async def returnToAdminPanel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('end adding new cloth', show_alert=False)
    async with state.proxy() as data:
        if callback.from_user.username is not None and callback.from_user.id != 292667494:
            data['user'] = f"@{callback.from_user.username}"
        else:
            data['user'] = '@biruytskovskynf'
        data['date'] = str(datetime.date.today())
        if callback.from_user.id in getAdmin().keys():
            try:
                await postNewClothInChannel(data)
            except Exception as e:
                AdminLogger.error('Post in general channel rejected by ' + type(e))
        DBcontroller.addCloth(data)
    await state.finish()
    await admLogin(callback.message, True)


async def postNewClothInChannel(clothInfoDict):
    media = types.MediaGroup()
    for i in range(len(clothInfoDict['photo'])):
        media.attach_photo(
            types.InputMediaPhoto(clothInfoDict['photo'][i],
                                  caption=getClothInfoForChannel(clothInfoDict) if i == 0 else ''))
    await bot.send_media_group(generalChannelId, media=media)


def registerHandlers():
    # cancel state handlers
    dp.register_message_handler(cancelAdd, commands='отмена', state=FSMAdmin.GroupStates['addCloth'])
    dp.register_message_handler(cancelAdd, Text(equals='отмена', ignore_case=True),
                                state=FSMAdmin.GroupStates['addCloth'])
    # admin panel handler
    dp.register_message_handler(admLogin, commands=['admin'])
    # add cloth handlers
    dp.register_callback_query_handler(startAdding, text='addCloth')
    dp.register_message_handler(chooseSubCategory, Text(equals=getCategories().keys(), ignore_case=False),
                                state=FSMAdmin.category)
    dp.register_message_handler(chooseBrand, state=FSMAdmin.subCategory)
    dp.register_message_handler(chooseName, state=FSMAdmin.brand)
    dp.register_message_handler(choosePrice, state=FSMAdmin.name)
    dp.register_message_handler(chooseSize, state=FSMAdmin.price)
    dp.register_message_handler(chooseCondition, state=FSMAdmin.size)
    dp.register_message_handler(choosePhoto, state=FSMAdmin.condition)
    dp.register_callback_query_handler(returnToAdminPanel, state=FSMAdmin.photo, text='returnToAdmin')
    dp.register_message_handler(endAddingCloth, content_types=['photo'], state=FSMAdmin.photo)
    ###
    InitLogger.info('admin handlers registered')
