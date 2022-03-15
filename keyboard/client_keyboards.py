from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

buttonLohCheck = KeyboardButton('Проверка на лоха')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(buttonLohCheck)
