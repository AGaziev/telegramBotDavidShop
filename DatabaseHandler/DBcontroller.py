from DatabaseHandler.firebaseConfigure import db
from DatabaseHandler.userInfo import setNoveltyToUsers
from LoggerHandler import DBLogger

# from keyboard import category as categoryList

showInfo = ['subCategory', 'brand', 'name', 'price', 'condition', 'photo', 'size', 'user', 'date']


def addCloth(data: dict):
    DBLogger.info(
        f'Adding new cloth in base {data["category"]},{data["subCategory"]} with name: {data["brand"]} \"{data["name"]}\"')
    db.child('CLOTHES').child(data['category']).child(data['subCategory']).push(
        {k: v for k, v in data.items() if k in showInfo})
    getNumberOfClothes([data['category'], data['subCategory']])
    setNoveltyToUsers(data['category'], data['subCategory'], True)
    updateAllClothesCounter()


def deleteCloth(path: list):
    DBLogger.info(
        f'Deleting cloth from base {path[0]},{path[1]} with id: {path[2]}')
    db.child(getDbPath(path)).remove()
    count = getNumberOfClothes([path[0], path[1]])
    if count == 0:
        setNoveltyToUsers(path[0], path[1], False)
    updateAllClothesCounter()


def getDbPath(path: list):
    dbPath = '/CLOTHES'
    for child in path:
        dbPath += f'/{child}'
    return dbPath


def getNumberOfClothes(path: list, justCheck=False):
    clothes = db.child(getDbPath(path)).get().each()
    if clothes is not None:
        count = len(clothes)
    else:
        count = 0
    if not justCheck:
        db.child('statistics/' + getDbPath(path)).set(count)
    return count


def getMainCategoryCount(category):
    categoryCount = 0
    if db.child('statistics/CLOTHES/' + category).get().each() is not None:
        for subCategoryCounter in db.child('statistics/CLOTHES/' + category).get().each():
            categoryCount += subCategoryCounter.val()
    return categoryCount


def updateAllClothesCounter():
    clothesCount = 0
    for category in db.child('statistics/CLOTHES').get().each():
        if category.key() != 'ALL':
            clothesCount += getMainCategoryCount(category.key())
    db.child('statistics/CLOTHES/ALL').set(clothesCount)
    DBLogger.info('Updated Counter of all clothes')
    return clothesCount


def getClothesList(path: list) -> dict:
    if db.child(getDbPath(path)).get().val() is None:
        return {}
    else:
        return db.child(getDbPath(path)).get().val()


def totalUpdate():
    for cat, subcat in categoryList.items():
        for sub in subcat:
            getNumberOfClothes([cat, sub])
    updateAllClothesCounter()


def getSellers():
    try:
        sellers = list(db.child('SideSellers').get().val().keys())
    except AttributeError:
        sellers = []
    return sellers


categoryList = {
    'Обувь': ('Кроссовки', 'Кеды', 'Тапки'),
    'Верх': ('Худи', 'Свитшот', 'Флиска', 'T-shirt', 'Майка', 'Куртка', 'Пальто', 'Бомбер', 'Спортивные', 'Polo', 'Рубашка'),
    'Низ': ('Спортивные', 'Обычные', 'Шорты', 'Джинсы')
}

# example = {'category': 'Обувь', 'subCategory': 'Кроссовки', 'brand': 'Nike', 'name': 'Monarch', 'price': 2000.0,
#            'condition': 'Отличное',
#            'photo': ['AgACAgIAAxkBAAIEnWI1DS_Sc-UfHR_S939ULbzFcZxPAALTvzEbEB-oSZkTqTje8FlOAQADAgADeQADIwQ'],
#            'size': 'M'}
# addCloth(example)
