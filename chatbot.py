import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory  # Import Sastrawi stemmer

from tensorflow.keras.models import load_model
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
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# Load NLP models and data
lemmatizer = WordNetLemmatizer()
stemmer = StemmerFactory().create_stemmer()
intents_data = db.child("intents").get().val()
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    sentence_words = [stemmer.stem(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    result = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    result.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in result:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    for intent_id, intent_data in intents_json.items():
        if intent_data['tag'] == tag:
            result = random.choice(intent_data['responses'])
            break
    return result

# print("Go! Bot is Running!")

# while True:
#     message = input("You: ")
#     if message.lower() == "quit":
#         break
#     intents_list = predict_class(message)
#     response = get_response(intents_list, intents_data)
#     print("Bot:", response)
