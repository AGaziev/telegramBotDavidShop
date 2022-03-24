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
        text += f'{subcategory} - {getNumberOfClothes([category, subcategory])}\n'
    return text

def getClothInfo(data: dict):
    name = (f'\"{data["name"]}\"' if data["name"] != '' else '')
    return f'{data["subCategory"]}\n' \
           f'{data["brand"]} {name}\"\n' \
           f'Стоимость: {data["price"]}\n' \
           f'Состояние: {data["condition"]}\n' \
           f'Размер: {data["size"]}\n'
