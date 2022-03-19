from DatabaseHandler.firebaseConfigure import db
from DatabaseHandler.statisticsCounters import clothesCount

showInfo = [ 'subCategory', 'brand','name', 'price', 'condition', 'photo', 'size']

def addCloth(data: dict):
    id = clothesCount.getVal()
    print(data)
    db.child('CLOTHES').child(data['category']).child(data['subCategory']).child(id).set({k:v for k,v in data.items() if k in showInfo})
    +clothesCount

def getNumberOfClothes(path: list):
    dbPath = '/CLOTHES'
    for child in path:
        dbPath += f'/{child}'
    print(db.child(dbPath).get().each())

getNumberOfClothes(['Обувь', 'Кроссовки'])

example = {'category': 'Обувь', 'subCategory': 'Кроссовки', 'brand': 'Nike', 'name': 'Monarch', 'price': 2000.0,
 'condition': 'Отличное',
 'photo': ['AgACAgIAAxkBAAIEnWI1DS_Sc-UfHR_S939ULbzFcZxPAALTvzEbEB-oSZkTqTje8FlOAQADAgADeQADIwQ'], 'size': 'M'}
# addCloth(example)