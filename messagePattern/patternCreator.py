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
        text += f'{subcategory} : {getNumberOfClothes([category, subcategory])}\n'
    return text
