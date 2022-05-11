from DatabaseHandler.firebaseConfigure import db
from LoggerHandler import DBLogger
import collections


def checkUserRegistration(id):  # check if user used a bot
    try:
        registeredId = db.child('userInfo').get().val().keys()
    except AttributeError:
        registeredId = []
    if id not in registeredId:
        noveltyListForNewUser = listForNewUser()
        db.child('userInfo').child(id).set(noveltyListForNewUser)
        DBLogger.info(f'New user registered to bot with id: {id}')
        return False
    else:
        return True


def listForNewUser():  # get list for new users depended on clothes counters (false if no cloth in subcategory
    categoryNewDict = {}
    for category, subCategory in categoryList.items():
        subDict = {}
        for sub in subCategory:
            subDict[sub] = bool(db.child(f'statistics/CLOTHES/{category}/{sub}').get().val())
        categoryNewDict[category] = subDict
    return categoryNewDict


def categoriesWithNew(id):  # get categories with new items
    id = str(id)
    categoryWithNew = []
    indicatorsForId = db.child('userInfo').child(id).get().val()
    for cat, subCatDict in indicatorsForId.items():
        if True in subCatDict.values():
            categoryWithNew.append(cat)
    return categoryWithNew


def subcatWithNew(id, category):  # get subcategories with new items
    id = str(id)
    subCatsWithNew = []
    indicatorsForId = db.child('userInfo').child(id).child(category).get().val()
    for subCat, isNew in indicatorsForId.items():
        if isNew:
            subCatsWithNew.append(subCat)
    return subCatsWithNew


def notNewAnymore(id, category, subCategory):  # falsing new for subcategory
    db.child('userInfo').child(id).child(category).child(subCategory).set(False)


categoryList = {
    'Обувь': ('Кроссовки', 'Кеды', 'Тапки'),
    'Верх': (
    'Худи', 'Свитшот', 'Флиска', 'T-shirt', 'Майка', 'Куртка', 'Пальто', 'Бомбер', 'Спортивные', 'Polo', 'Рубашка'),
    'Низ': ('Спортивные', 'Обычные', 'Шорты', 'Джинсы')
}

categoryNewList = {
    'Обувь': {'Кроссовки': True, 'Кеды': True, 'Тапки': True},
    'Верх': {'Худи': True, 'Свитшот': True, 'Флиска': True, 'T-shirt': True, 'Майка': True, 'Куртка': True,
             'Пальто': True, 'Бомбер': True, 'Спортивные': True, 'Polo': True, 'Рубашка': True},
    'Низ': {'Спортивные': True, 'Обычные': True, 'Шорты': True, 'Джинсы': True}
}