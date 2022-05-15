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
    getNumberOfClothes(data['category'], data['subCategory'])
    setNoveltyToUsers(data['category'], data['subCategory'], True)
    updateAllClothesCounter()


def deleteCloth(category, subCategory, clothId):
    DBLogger.info(
        f'Deleting cloth from base {category}, {subCategory} with id: {clothId}')
    db.child('CLOTHES').child(category).child(subCategory).child(clothId).remove()
    count = getNumberOfClothes(category, subCategory)
    if count == 0:
        setNoveltyToUsers(category, subCategory, False)
    updateAllClothesCounter()


def getNumberOfClothes(category, subCategory, justCheck=False) -> int:
    clothes = db.child('CLOTHES').child(category).child(subCategory).get().each()
    if clothes is not None:
        count = len(clothes)
    else:
        count = 0
    if not justCheck:
        db.child('categories').child(category).child(subCategory).set(count)
    return count


def getMainCategoryCount(category) -> int:
    categoryCount = 0
    countersOfCategory = db.child('categories').child(category).get().each()
    if countersOfCategory is not None:
        for subCategoryCounter in countersOfCategory:
            categoryCount += subCategoryCounter.val()
    return categoryCount


def updateAllClothesCounter():
    clothesCount = 0
    for category in getCategories().keys():
        clothesCount += getMainCategoryCount(category)
    db.child('statistics/counterOfItemsInStore').set(clothesCount)
    DBLogger.info('Updated Counter of all clothes')
    return clothesCount


def getClothesList(category, subCategory) -> dict:
    clothesList = db.child('CLOTHES').child(category).child(subCategory).get().val()
    if clothesList is None:
        return {}
    else:
        return clothesList


def totalUpdate():
    for cat, subcat in getCategories().items():
        for sub in subcat.keys():
            getNumberOfClothes(cat, sub)
    updateAllClothesCounter()


def getSellersID() -> list:
    try:
        sellers = list(db.child('sellers').child('sideSellers').get().val().keys())
    except AttributeError:
        sellers = []
    return sellers

def getAdmin() -> dict:
    admins = {}
    try:
        tempAdmins = dict(db.child('sellers').child('admins').get().val())
    except TypeError:
        tempAdmins = {}
    for id, name in tempAdmins.items():
        admins[int(id)] = name
    return admins


def getCategories() -> dict:
    try:
        categoryList = dict(db.child('categories').get().val())
    except TypeError:
        categoryList = {}
    return categoryList

# print(getSellersID())
# print(getCategories())
# print(getAdmin())
# totalUpdate()
# getMainCategoryCount('Верх')
# categoryList = {
#     'Обувь': ('Кроссовки', 'Кеды', 'Тапки'),
#     'Верх': (
#     'Худи', 'Свитшот', 'Флиска', 'T-shirt', 'Майка', 'Куртка', 'Пальто', 'Бомбер', 'Спортивные', 'Polo', 'Рубашка',
#     'Лонгслив'),
#     'Низ': ('Спортивные', 'Обычные', 'Шорты', 'Джинсы')
# }
