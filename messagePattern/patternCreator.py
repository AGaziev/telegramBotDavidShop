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
    text = 'Количество вещей в каждой подкатегории\n'
    for subcategory in catList[category]:
        count = getNumberOfClothes([category, subcategory], justCheck=True)
        if count != 0:
            text += f'{subcategory} - {count}\n'
    return text


def getClothInfo(data: dict, current, total):
    name = (f'\"{data["name"]}\"' if data["name"] != '' else '')
    return f'{current}/{total}\n' \
           f'{data["subCategory"]}\n' \
           f'{data["brand"]} {name}\n' \
           f'Стоимость: {data["price"]}\n' \
           f'Состояние: {data["condition"]}\n' \
           f'Размер: {data["size"]}\n'
