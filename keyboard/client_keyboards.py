from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

start = ['Каталог', 'Информация']
startBut = (KeyboardButton(text) for text in start)

kbStart = ReplyKeyboardMarkup(resize_keyboard=True)

kbStart.add(*startBut)

# Словарь с клавиатурами
clientKbDict = {
    'start': kbStart
}
