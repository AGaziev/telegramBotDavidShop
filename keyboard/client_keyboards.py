from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

buttonLohCheck = KeyboardButton('Проверка на лоха')

kbStart = ReplyKeyboardMarkup(resize_keyboard=True)

kbStart.add(buttonLohCheck)
