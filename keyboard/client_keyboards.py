from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

from keyboard import other_keyboards

start = ['Каталог', 'Информация']
startBut = (KeyboardButton(text) for text in start)
kbStart = ReplyKeyboardMarkup(resize_keyboard=True)
kbStart.add(*startBut)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

mainBut = (InlineKeyboardButton(text, callback_data=text) for text in other_keyboards.category.keys())
ikbMain = InlineKeyboardMarkup()
ikbMain.add(*mainBut)

shoeBut = (InlineKeyboardButton(text, callback_data=text) for text in other_keyboards.category['Обувь'])
ikbShoe = InlineKeyboardMarkup()
ikbShoe.add(*shoeBut)

upBut = (InlineKeyboardButton(text, callback_data=text) for text in other_keyboards.category['Верх'])
ikbUp = InlineKeyboardMarkup()
ikbUp.add(*upBut)

downBut = (InlineKeyboardButton(text, callback_data=text) for text in other_keyboards.category['Низ'])
ikbDown = InlineKeyboardMarkup()
ikbDown.add(*downBut)

# flip = [
#     ('<<', 'previous'),
#     ('>>', 'next'),
#     ('Назад', 'back')
# ]
# flipBut = (InlineKeyboardButton(text, callback_data=data) for text, data in flip)
# ikbFlip = InlineKeyboardMarkup()
# ikbFlip.add(*flipBut)

# Словарь с клавиатурами
clientKbDict = {
    'start': kbStart,
    # 'flip': ikbFlip,
    'main': ikbMain,
    'Обувь': ikbShoe,
    'Верх': ikbUp,
    'Низ': ikbDown
}
