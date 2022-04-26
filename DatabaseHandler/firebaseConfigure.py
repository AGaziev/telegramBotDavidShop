import pyrebase
import os
from cryptocode import decrypt

key = open('secondroomdb-bf3f10c9f6a1.json', 'w')
key.write(decrypt(os.getenv("SAKey"), os.getenv("SAPasswordToEncrypt")))
key.close()

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

# if os.path.isfile(os.getenv("SAKeyPath")):
#     os.remove(os.getenv("SAKeyPath"))
# else:
#     print('FILE WITH CREDENTIALS NOT FOUND')
