from create_bot import bot, dp, fsm
from keyboard import categoryList, ikbAdmin
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup

adminId = {1256578670: 'David',
           292667494: 'Alan'}


class FSMAdmin(StatesGroup):
    category = State()
    subCategory = State()
    brand = State()
    name = State()
    price = State()
    photo = State()


# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel(message: types.Message):
    if message.from_user.id in adminId.keys():
        print('cancel admin panel')
    await message.reply('Возвращаюсь...')


# @dp.callback_query_handler(text='addCloth')
async def chooseSubCategory(callback: types.CallbackQuery):
    pass


# @dp.message_handler(commands=['admin'], state=None)
async def admStart(message: types.Message):
    if message.from_user.id in adminId.keys():
        print(adminId[message.from_user.id], 'on admin panel')
        await bot.send_message(message.chat.id, 'Успешный вход на панель админа', reply_markup=ikbAdmin)
    else:
        await message.reply('Недостаточно прав')


@dp.callback_query_handler(text='addCloth')
async def chooseCategory(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, 'Выберите категорию', reply_markup=kbCategory)
    await call.answer('start adding new cloth', show_alert=False)


def register_handlers():
    dp.register_message_handler(cancel, commands='отмена')
    dp.register_message_handler(cancel, Text(equals='отмена', ignore_case=True))
    dp.register_message_handler(admStart, commands=['admin'])
    dp.register_callback_query_handler(chooseSubCategory, text='addCloth')
    print('registered')
