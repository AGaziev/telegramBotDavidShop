import re
from DatabaseHandler import db

class Counter:
    def __init__(self, path):
        self.path = path
        self.name = re.findall(f'(.+)/(.*)$', path)[0][1]
        self.value = db.child(self.path).get().val()

    def getVal(self):
        return db.child(self.path).get().val()

    def setVal(self,val):
        db.child(self.path).set(val)

    def __neg__(self):
        temp = self.getVal()
        self.setVal(temp-1)

    def __pos__(self):
        temp = self.getVal()
        self.setVal(temp+1)


clothesCount = Counter('/statistics/clothesCount')
