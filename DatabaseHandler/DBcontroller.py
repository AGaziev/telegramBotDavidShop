from DatabaseHandler.firebaseConfigure import db
from DatabaseHandler.statisticsCounters import clothesCount


def addCloth(data: dict):
    id = clothesCount.getVal()
    print(data['category'])
    db.child('CLOTHES').child(data['category']).child(data['subCategory']).child(id).push('')


example = {'category': 'Обувь', 'subCategory': 'Кроссовки', 'brand': 'Nike', 'name': 'Monarch', 'price': 2000.0,
 'condition': 'Отличное',
 'photo': ['AgACAgIAAxkBAAIEnWI1DS_Sc-UfHR_S939ULbzFcZxPAALTvzEbEB-oSZkTqTje8FlOAQADAgADeQADIwQ']}
addCloth(example)