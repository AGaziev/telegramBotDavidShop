replyPatterns = {
    'toStart': 'Введите /start для открытия контекстного меню'
}

from DatabaseHandler import getMainCategoryCount, getNumberOfClothes
from DatabaseHandler import categoriesWithNew, subcatWithNew
from DatabaseHandler import getCategories
import datetime


def getCategoryInfo(id):
    text = 'Количество вещей в каждой категории\n'
    catWithNew = categoriesWithNew(id)
    categoriesDict = getCategories()
    for category in categoriesDict.keys():
        text += f'{category} - {getMainCategoryCount(category)} {"NEW!" if category in catWithNew else ""}\n'
    return text


def getSubCategoryInfo(category, id):
    start = 'Количество вещей в каждой подкатегории\n'
    text = ''
    subcatsNew = subcatWithNew(id, category)
    categoriesDict = getCategories()
    for subcategory in categoriesDict[category]:
        count = getNumberOfClothes(category, subcategory,
                                   justCheck=True)
        if count != 0:
            text += f'{subcategory} - {count} {"NEW!" if subcategory in subcatsNew else ""}\n'
    if text == '':
        text = 'Нет вещей в выбранной категории\n'

    return start + text


def getClothInfo(data: dict, current, total):
    try:
        date = data['date'].split('-')
        date = list(map(int, date))
        dateDiff = (datetime.date.today() - datetime.date(*date)).days
        if dateDiff < 3:
            dateText = ' NEW!'
        else:
            dateText = ''
    except Exception as e:
        dateText = ''
    name = (f'\"{data["name"]}\"' if data["name"] != 'None' else '')
    return f'{current}/{total}\n' \
           f'{data["subCategory"]}{dateText}\n' \
           f'{data["brand"]} {name}\n\n' \
           f'{data["price"]}\n\n' \
           f'Состояние: {data["condition"]}\n' \
           f'Размер: {data["size"]}\n' \
           f'За покупкой {data["user"]}'

def getClothInfoForChannel(data:dict):
    name = (f'\"{data["name"]}\"' if data["name"] != 'None' else '')
    return f'{data["brand"]}\n\n' \
           f'{data["subCategory"]} {name}\n\n' \
           f'{data["size"]}\n\n' \
           f'{data["price"]}\n\n' \
           f'За покупкой {data["user"]}'
