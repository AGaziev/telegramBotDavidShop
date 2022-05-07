from create_bot import bot, dp

from aiogram import types
from keyboard import ikbSideSellersPanel

from DatabaseHandler import getSellers
from LoggerHandler import SellerLogger, InitLogger


# @dp.message_handler(commands=['login'], state=None)
async def selLogin(message: types.Message):
    sellers = getSellers()
    if message.from_user.id in sellers:
        SellerLogger.info(f'{message.from_user.username} entered admin panel')
        await bot.send_message(message.chat.id, 'Успешный вход',
                               reply_markup=ikbSideSellersPanel)
    else:
        await message.reply('У вас нет прав.')


def sideSellerRegisterHandlers():
    dp.register_message_handler(selLogin, commands=['login'], state=None)
    InitLogger.info('sideSellers handlers registered')
