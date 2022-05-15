from DatabaseHandler.firebaseConfigure import db
from aiogram import types
from LoggerHandler import DBLogger
import collections


def checkUserRegistration(id, message):  # check if user used a bot
    try:
        registeredId = db.child('userInfo').get().val().keys()
    except AttributeError:
        registeredId = []
    if id not in registeredId:
        noveltyListForNewUser = listForNewUser()
        db.child('userInfo').child(id).child('noveltyCheck').set(noveltyListForNewUser)
        db.child('userInfo').child(id).update({'username': f'{getUserInfo(message)}'})
        DBLogger.info(f'New user registered to bot with id: {id}')
        return False
    else:
        return True

def getUserInfo(message:types.Message):
    info = ''
    if message.from_user.username is not None:
        info+=message.from_user.username + ' '
    if message.from_user.first_name is not None:
        info+=message.from_user.first_name + ' '
    if message.from_user.last_name is not None:
        info+message.from_user.last_name
    return info



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
    indicatorsForId = db.child('userInfo').child(id).child('noveltyCheck').get().val()
    for cat, subCatDict in indicatorsForId.items():
        if True in subCatDict.values():
            categoryWithNew.append(cat)
    return categoryWithNew


def subcatWithNew(id, category):  # get subcategories with new items
    id = str(id)
    subCatsWithNew = []
    indicatorsForId = db.child('userInfo').child(id).child('noveltyCheck').child(category).get().val()
    for subCat, isNew in indicatorsForId.items():
        if isNew:
            subCatsWithNew.append(subCat)
    return subCatsWithNew


def notNewAnymore(id, category, subCategory):  # falsing new for subcategory
    db.child('userInfo').child(id).child('noveltyCheck').child(category).child(subCategory).set(False)


def setNoveltyToUsers(category,subCategory, novelty):
    listOfUsersId = db.child('userInfo').get().val().keys()
    for userId in listOfUsersId:
        db.child(f'userInfo/{userId}/noveltyCheck/{category}/{subCategory}').set(novelty)


categoryList = {
    'Обувь': ('Кроссовки', 'Кеды', 'Тапки'),
    'Верх': (
    'Худи', 'Свитшот', 'Флиска', 'T-shirt', 'Майка', 'Куртка', 'Пальто', 'Бомбер', 'Спортивные', 'Polo', 'Рубашка', 'Лонгслив'),
    'Низ': ('Спортивные', 'Обычные', 'Шорты', 'Джинсы')
}

categoryNewList = {
    'Обувь': {'Кроссовки': True, 'Кеды': True, 'Тапки': True},
    'Верх': {'Худи': True, 'Свитшот': True, 'Флиска': True, 'T-shirt': True, 'Майка': True, 'Куртка': True,
             'Пальто': True, 'Бомбер': True, 'Спортивные': True, 'Polo': True, 'Рубашка': True},
    'Низ': {'Спортивные': True, 'Обычные': True, 'Шорты': True, 'Джинсы': True}
}