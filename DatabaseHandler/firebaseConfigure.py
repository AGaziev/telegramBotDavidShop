import pyrebase
import os
import json
from cryptocode import decrypt

firebaseConfig = {
    'apiKey': os.getenv("FIREBASE_API_KEY"),
    'authDomain': os.getenv("FIREBASE_AUTH_DOMAIN"),
    'databaseURL': os.getenv("FIREBASE_DATABASE_URL"),
    'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET"),
    'serviceAccount': json.loads(decrypt(os.getenv("SERVICEACCOUNT_KEY"), os.getenv("SERVICEACCOUNT_PASSWORD_TO_ENCRYPT")))
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()
