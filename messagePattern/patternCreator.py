replyPatterns = {
    'toStart': 'Введите /start для открытия контекстного меню'
}

from DatabaseHandler import getMainCategoryCount, getNumberOfClothes
from keyboard import category as catList


def getCategoryInfo():
    text = 'Количество вещей в каждой категории\n'
    for category in catList.keys():
        text += f'{category} - {getMainCategoryCount(category)}\n'
    return text


def getSubCategoryInfo(category):
    start = 'Количество вещей в каждой подкатегории\n'
    text = ''
    for subcategory in catList[category]:
        count = getNumberOfClothes([category, subcategory],
                                   justCheck=True)
        if count != 0:
            text += f'{subcategory} - {count}\n'
    if text == '':
        text = 'Нет вещей в выбранной категории\n'

    return start + text


def getClothInfo(data: dict, current, total):
    name = (f'\"{data["name"]}\"' if data["name"] != 'None' else '')
    return f'{current}/{total}\n' \
           f'{data["subCategory"]}\n' \
           f'{data["brand"]} {name}\n\n' \
           f'{data["price"]}\n\n' \
           f'Состояние: {data["condition"]}\n' \
           f'Размер: {data["size"]}\n' \
           f'За покупкой {data["user"]}'
