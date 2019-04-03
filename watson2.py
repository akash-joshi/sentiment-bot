import watson_developer_cloud
import json
from flask import Flask, session, redirect, url_for, escape, request


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
    response = ""
    question1 = ""
    question2 = ""

    with open('dialogs.txt') as csv_file:
        csv_reader = csv.reader(csv_file)
        questnos = sum(1 for row in csv_reader)
        #questnos = 11
        idx = 0
        for row in csv_reader:
            if(row[0] == quest):
                if(idx == questnos-1):
                    response = ""
                elif idx == questnos-2:
                    question1 = next(csv_reader)[1]
                else :
                    question1 = next(csv_reader)[1]
                    question2 = next(csv_reader)[1]
                break
            idx += 1
                        
    response = json.dumps({'quest1': quest1, 'quest2': quest2})
    return question1, question2

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
    
    question1, question2 = suggest_quest(response["output"]['generic'][0]['text'])

    resp_json = json.dumps({'answer': response["output"]['generic'][0]['text'], 'rec_q1': question1, 'rec_q2': question2})
    print(resp_json)
    return  resp_json


service = init_watson(version, iam_apikey, url)

if __name__ == "__main__":
    app.run()    

