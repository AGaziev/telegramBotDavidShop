import pyrebase
import os
import json
from cryptocode import decrypt

firebaseConfig = {
    'apiKey': os.getenv("fbApiKey"),
    'authDomain': os.getenv("fbAuthDomain"),
    'databaseURL': os.getenv("fbDatabaseURL"),
    'storageBucket': os.getenv("fbStorageBucket"),
    'serviceAccount': json.loads(decrypt(os.getenv("SAKey"), os.getenv("SAPasswordToEncrypt")))
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()
