from DatabaseHandler.firebaseConfigure import db

showInfo = ['subCategory', 'brand', 'name', 'price', 'condition', 'photo', 'size']


def addCloth(data: dict):
    # print(data)
    db.child('CLOTHES').child(data['category']).child(data['subCategory']).push(
        {k: v for k, v in data.items() if k in showInfo})
    print('kek')
    getNumberOfClothes([data['category'], data['subCategory']])
    updateAllClothesCounter()




def getDbPath(path: list):
    dbPath = '/CLOTHES'
    for child in path:
        dbPath += f'/{child}'
    return dbPath


def getNumberOfClothes(path: list):
    count = 0
    if db.child(getDbPath(path)).get().each() is not None:
        count = len(db.child(getDbPath(path)).get().each())
    print(count)
    print(path)
    db.child('statistics/'+getDbPath(path)).set(count)
    return count


def getMainCategoryCount(category):
    categoryCount = 0
    for subCategoryCounter in db.child('statistics/CLOTHES/' + category).get().each():
        categoryCount += subCategoryCounter.val()
    return categoryCount


def updateAllClothesCounter():
    clothesCount = 0
    for category in db.child('statistics/CLOTHES').get().each():
        if category.key() != 'ALL':
            clothesCount += getMainCategoryCount(category.key())
    db.child('statistics/CLOTHES/ALL').set(clothesCount)
    return clothesCount

example = {'category': 'Обувь', 'subCategory': 'Кроссовки', 'brand': 'Nike', 'name': 'Monarch', 'price': 2000.0,
           'condition': 'Отличное',
           'photo': ['AgACAgIAAxkBAAIEnWI1DS_Sc-UfHR_S939ULbzFcZxPAALTvzEbEB-oSZkTqTje8FlOAQADAgADeQADIwQ'],
           'size': 'M'}
# addCloth(example)
