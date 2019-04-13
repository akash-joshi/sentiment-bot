import watson_developer_cloud
import json
from flask import Flask, session, redirect, url_for, escape, request
import random
import pandas as pd

version = '2018-11-08'
iam_apikey = 'wQ_1OrWKz-2ZTx4rI4AzRxOsuiTAj2F4E5vTHLMZ_r0r'
url = 'https://gateway-lon.watsonplatform.net/assistant/api'
assistant_id = '8565e9a4-f45f-43b3-b87e-e54c4dbfa754'


def init_watson(version, iam_apikey, url):
    service = watson_developer_cloud.AssistantV2(
        version = version,
        iam_apikey = iam_apikey,
        url = url
        )
    return service
        
def suggest_quest(intent):
    question1, question2 = "", ""
    question3, question4, question5 = "", "", ""
    #print(intent)
    df = pd.read_csv("dialogs.txt", sep=",", header=None)
    for idx, row in enumerate(df.values):
        if(row[0] == intent):
            question1 = df.values[(idx+1) % len(df)][1]
            question2 = df.values[(idx+2) % len(df)][1]
            number = list(range(0, (idx+1) % len(df))) + list(range((idx+2) % len(df), len(df)))
            question3 = df.values[random.choice(number)][1]
            question4 = df.values[random.choice(number)][1]
            question5 = df.values[random.choice(number)][1]
            print (question1, question2, question3, question4, question5)

    return question1, question2, question3, question4, question5

app = Flask(__name__)
app.secret_key = "Secret_Key"

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return redirect(url_for('message'))
    return "<a href='/create_session'>login</a>"

@app.route('/create_session', methods = ['POST'])
def create_session():
    service.set_default_headers({'x-watson-learning-opt-out': "true"})
    response = service.create_session(
        assistant_id = assistant_id
        ).get_result()
    
    sessid = response['session_id']
    return sessid

@app.route('/delete_session',methods=['POST'])
def delete_session():
    got = request.get_json(force=True)
    session_id = got['session_id']
    response = service.delete_session(
        assistant_id = assistant_id,
        session_id = session_id
        ).get_result()

    return 'ok'

@app.route('/message', methods = ['POST'])
def message():
    got = request.get_json(force=True)
    emotion = got['emotion']
    message = str(got['message'])
    response = service.message(
        assistant_id = assistant_id,
        session_id = got['session_id'],
        input={
            'message_type': 'text',
            'text': message + "," + emotion
            }
        ).get_result()
    
    question1, question2, question3, question4, question5 = suggest_quest(response["output"]['intents'][0]['intent'])

    resp_json = json.dumps({'answer': response["output"]['generic'][0]['text'], 'rec_q1': question1, 'rec_q2': question2, 'rec_q3': question3, 'rec_q4': question4, 'rec_q5': question5})
    print(resp_json)
    return resp_json


service = init_watson(version, iam_apikey, url)

if __name__ == "__main__":
    app.run()    

