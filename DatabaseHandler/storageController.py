from firebaseConfigure import storage


def uploadClothImage(pathToImage):
    storage.child('clothes').put(pathToImage)
    return storage.child('clothes').get_url()


def getClothImageURI(name):
    storage.child('cloth').get_url(name)

