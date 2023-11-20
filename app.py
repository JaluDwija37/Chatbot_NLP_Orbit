from flask import Flask, render_template, request, jsonify, redirect, url_for
# Import the get_answer function from chatbot.py
from chatbot import get_response, predict_class, intents_data
import pyrebase
import subprocess
import os

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

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('index_admin.html')


@app.route('/dashboard')
def dashboard():
    intents = db.child('intents').get()

    intent_data = []

    if intents:
        # Convert the PyreResponse object to a standard Python dictionary
        intents_dict = intents.val()
        if intents_dict:
            # Loop through the dictionary and append each intent to the list
            for intent_id, intent in intents_dict.items():
                intent_data.append({
                    'key': intent_id,
                    'tag': intent['tag'],
                    'patterns': intent['pattern'],
                    'responses': intent['responses']
                })

    return render_template('dashboard.html', intent_data=intent_data)


@app.route('/ask', methods=['POST'])
def ask():
    message = request.form['user_question']
    ints = predict_class(message)
    response = get_response(ints, intents_data)
    # Change 'user_question' to 'message'
    return jsonify({'response': response})

# This is Retrain
# @app.route('/run_python_script', methods=['POST'])
# def run_python_script():
#     try:
#         # Replace 'your_script.py' with the actual filename of your Python script
#         subprocess.run(['python', 'training2.py'])

#         # Restart the Flask server
#         os.kill(os.getpid(), 9)  # Send a signal to terminate the current process

#         return 'Python script executed successfully. Flask server is restarting...'
#     except Exception as e:
#         return f'Error executing Python script: {str(e)}'


@app.route('/insert_data', methods=['POST'])
def insert_data():
    tag = request.form['tag']
    pattern = request.form['pattern']
    responses = request.form['responses']
    pattern_split = pattern.split(';')
    responses_split = responses.split(';')
    data = {
        "tag": tag,
        "pattern": pattern_split,
        "responses": responses_split,
    }

    db.child("intents").push(data)  # Pass 'intents' to the function
    print("data diinput")
    return redirect(url_for('dashboard'))


@app.route('/update_data', methods=['POST'])
def update_data():
    update_tag = request.form['tag']
    update_pattern = request.form['patterns']
    update_responses = request.form['responses']
    pattern_split = update_pattern.split(';')
    responses_split = update_responses.split(';')

    data = {
        "tag": update_tag,
        "pattern": pattern_split,
        "responses": responses_split,
    }

    intents_data = db.child("intents").get()

    key = None
    for data_node in intents_data.each():
        if data_node.val()['tag'] == update_tag:
            key = data_node.key()
            break  # Exit the loop once we find the key

    if key is not None:
        # Convert data to a JSON-serializable form (e.g., using dictionary comprehension)
        serializable_data = {
            "tag": data['tag'],
            "pattern": data['pattern'],
            "responses": data['responses'],
        }

        # Update the database with the serializable_data
        db.child("intents").child(key).update(serializable_data)

    return redirect(url_for('dashboard'))


@app.route('/delete_data', methods=['POST'])
def delete_data():
    delete_tag = request.form['delete_tag']

    intents_data = db.child("intents").get()

    key = None
    for data_node in intents_data.each():
        if data_node.val()['tag'] == delete_tag:
            key = data_node.key()
            break  # Exit the loop once we find the key

    if key is not None:

        db.child("intents").child(key).remove()

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
