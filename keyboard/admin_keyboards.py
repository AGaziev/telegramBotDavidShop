from DatabaseHandler import getCategories
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

# conditions variants
conditions = ('Хорошее', 'Отличное')
kbCondition = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
conditionButtons = (KeyboardButton(text=text) for text in conditions)
kbCondition.add(*conditionButtons)

kbCategory = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
categoryButtons = (KeyboardButton(text) for text in getCategories().keys())
kbCategory.add(*categoryButtons)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# admin panel keyboard
admPanel = [
    ('Добавить', 'addCloth')
]
ikbAdmin = InlineKeyboardMarkup()
rowButtons = (InlineKeyboardButton(text, callback_data=data) for text, data in admPanel)
ikbAdmin.add(*rowButtons)

# dictionary of keyboards
adminKbDict = {
    'adminPanelInline': ikbAdmin,
    'condition': kbCondition,
    'main': kbCategory
}


def getSubCategoryKbAdmin(category):
    subCatKb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    for subCategory in getCategories()[category]:
        subCatKb.insert(KeyboardButton(subCategory))
    return subCatKb
