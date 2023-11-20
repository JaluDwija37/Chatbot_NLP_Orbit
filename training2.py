import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
from nltk.stem import WordNetLemmatizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
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

lemmatizer = WordNetLemmatizer()
stemmer = StemmerFactory().create_stemmer()

# Load intents from JSON
intents_data = db.child("intents").get().val()
# print(intents_data.val())
words = []
classes = []
documents = []
ignoreLetters = ['?', '!', '.', ',']

for intent_data in intents_data.values():
    for pattern in intent_data['pattern']:
        wordList = nltk.word_tokenize(pattern)
        words.extend(wordList)
        documents.append((wordList, intent_data['tag']))
        if intent_data['tag'] not in classes:
            classes.append(intent_data['tag'])

words = [lemmatizer.lemmatize(word)
         for word in words if word not in ignoreLetters]

# Use Sastrawi to stem the words
words = [stemmer.stem(word) for word in words]

words = sorted(set(words))
classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
outputEmpty = [0] * len(classes)

for document in documents:
    bag = []
    wordPatterns = document[0]
    wordPatterns = [lemmatizer.lemmatize(
        word.lower()) for word in wordPatterns]

    # Use Sastrawi to stem the word patterns
    wordPatterns = [stemmer.stem(word) for word in wordPatterns]

    for word in words:
        bag.append(1) if word in wordPatterns else bag.append(0)

    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1
    training.append(bag + outputRow)

random.shuffle(training)
training = np.array(training)

trainX = training[:, :len(words)]
trainY = training[:, len(words):]

model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(
    128, input_shape=(len(trainX[0]),), activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(len(trainY[0]), activation='softmax'))

sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd, metrics=['accuracy'])

model.fit(trainX, trainY, epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5')
print('Done')
