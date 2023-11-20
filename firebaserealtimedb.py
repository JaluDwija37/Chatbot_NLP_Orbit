import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyBpjiMsralXRn3rCQMeCRhJ_kSdTIcI3mQ",
  'authDomain': "chatbot-ai-32ffc.firebaseapp.com",
  'databaseURL': "https://chatbot-ai-32ffc-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "chatbot-ai-32ffc",
  'storageBucket': "chatbot-ai-32ffc.appspot.com",
  'messagingSenderId': "709829319061",
  'appId': "1:709829319061:web:37aae3f0612a0c487b7e9c",
  'measurementId': "G-QXQCFST5CC"
};

firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()

#this is add data
# data = {
#     "tag": "goodbye",
#     "pattern": ["sampai jumpa",
#                 "Sampai nanti",
#                 "Selamat tinggal",
#                 "Saya pergi",
#                 "Semoga harimu menyenangkan",
#                 "bye",
#                 "Cao",
#                 "sampai jumpa lagi",
#                 "terima kasih"],
#     "responses": ["Sedih melihatmu pergi :(",
#                 "Sampai jumpa nanti",
#                 "Selamat tinggal!"],
# }

# db.child("intents").push(data)


#retrieve data
intents=db.child("intents").get()
print(intents.val())
print("Data imported successfully.")