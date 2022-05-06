from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from DatabaseHandler import getNumberOfClothes

from keyboard import other_keyboards

start = ['Каталог', 'Информация']
startBut = (KeyboardButton(text) for text in start)
kbStart = ReplyKeyboardMarkup(resize_keyboard=True)
kbStart.add(*startBut)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

backBut = InlineKeyboardButton('Назад', callback_data='back')
backCatBut = InlineKeyboardButton('Назад', callback_data='backToCat')

mainBut = (InlineKeyboardButton(text, callback_data=text) for text in other_keyboards.category.keys())
ikbMain = InlineKeyboardMarkup()
ikbMain.add(*mainBut).add(backBut)


# shoeBut = (InlineKeyboardButton(text, callback_data=text) for text in other_keyboards.category['Обувь'])
# ikbShoe = InlineKeyboardMarkup()
# ikbShoe.add(*shoeBut).add(backBut)
#
# upBut = (InlineKeyboardButton(text, callback_data=text) for text in other_keyboards.category['Верх'])
# ikbUp = InlineKeyboardMarkup()
# ikbUp.add(*upBut).add(backBut)
#
# downBut = (InlineKeyboardButton(text, callback_data=text) for text in other_keyboards.category['Низ'])
# ikbDown = InlineKeyboardMarkup()
# ikbDown.add(*downBut).add(backBut)


# flip = [
#     ('<<', 'previous'),
#     ('>>', 'next'),
#     ('Назад', 'back')
# ]
# flipBut = (InlineKeyboardButton(text, callback_data=data) for text, data in flip)
# ikbFlip = InlineKeyboardMarkup()
# ikbFlip.add(*flipBut)

def getSubCategoryKb(category):
    subCatKb = InlineKeyboardMarkup(row_width=3)
    for subCategory in other_keyboards.category[category]:
        if getNumberOfClothes([category, subCategory]) != 0:
            subCatKb.insert(InlineKeyboardButton(subCategory, callback_data=subCategory))
    subCatKb.row(backCatBut)
    return subCatKb


# Словарь с клавиатурами
clientKbDict = {
    'start': kbStart,
    # 'flip': ikbFlip,
    'main': ikbMain,
    # 'Обувь': ikbShoe,
    # 'Верх': ikbUp,
    # 'Низ': ikbDown
}
