from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

category = {
    'Обувь': ['Кроссовки', 'Кеды', 'Тапки'],
    'Верх': ['Худи', 'Свитшот', 'Флиска', 'T-shirt', 'Майка', 'Куртка', 'Пальто', 'Бомбер'],
    'Низ': ['Спортивные', 'Обычные']
}
# buttons
kbMainButs = (KeyboardButton(text=text) for text in category.keys())
kbShoeButs = (KeyboardButton(text=text) for text in category['Обувь'])
kbUpButs = (KeyboardButton(text=text) for text in category['Верх'])
kbDownButs = (KeyboardButton(text=text) for text in category['Низ'])
# keyboards
kbMainCat = ReplyKeyboardMarkup(resize_keyboard=True)
kbMainCat.add(*kbMainButs)

kbShoeCat = ReplyKeyboardMarkup(resize_keyboard=True)
kbShoeCat.add(*kbShoeButs)

kbDownCat = ReplyKeyboardMarkup(resize_keyboard=True)
kbDownCat.add(*kbDownButs)

kbUpCat = ReplyKeyboardMarkup(resize_keyboard=True)
kbUpCat.add(*kbUpButs)

# inline kbs
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# dict with keyboards
otherKbDict = {
    'main': kbMainCat,
    'Обувь': kbShoeCat,
    'Верх': kbUpCat,
    'Низ': kbDownCat
}
# in real life for the callback_data the callback data factory should be used
# here the raw string is used for the simplicity
# row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
