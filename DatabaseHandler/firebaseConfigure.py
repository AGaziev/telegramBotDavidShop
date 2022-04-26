import pyrebase
import os
from cryptocode import decrypt

with open('secondroomdb-bf3f10c9f6a1.json', 'w') as key:
    key.write(decrypt(os.getenv("SAKey"), os.getenv("SAPasswordToEncrypt")))

firebaseConfig = {
    'apiKey': os.getenv("fbApiKey"),
    'authDomain': os.getenv("fbAuthDomain"),
    'databaseURL': os.getenv("fbDatabaseURL"),
    'storageBucket': os.getenv("fbStorageBucket"),
    'serviceAccount': os.getenv("SAKeyPath")
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()

if os.path.isfile(os.getenv("SAKeyPath")):
    os.remove(os.getenv("SAKeyPath"))
else:
    print('FILE WITH CREDENTIALS NOT FOUND')
