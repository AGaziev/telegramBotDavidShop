import pyrebase
firebaseConfig = {
  'apiKey': "AIzaSyBWxii4w4pFJlGhRWVxUybF6kqXhvfzgcE",
  'authDomain': "secondroomdb.firebaseapp.com",
  'databaseURL': "https://secondroomdb-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "secondroomdb",
  'storageBucket': "secondroomdb.appspot.com",
  'messagingSenderId': "494102226364",
  'appId': "1:494102226364:web:aac006cb16eb85661577b9",
  'measurementId': "G-GE6KCNJS48"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()
