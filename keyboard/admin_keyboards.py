from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admButtons = [
    ('Добавить', 'addCloth')
]

ikbAdmin = InlineKeyboardMarkup()
rowButtons = (InlineKeyboardButton(text,callback_data=data) for text,data in admButtons)
ikbAdmin.add(*rowButtons)
