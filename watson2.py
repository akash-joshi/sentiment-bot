import watson_developer_cloud
import json
from flask import Flask, session, redirect, url_for, escape, request
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


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

def transcribe_gcs_long(file_path):
    client = speech.SpeechClient.from_service_account_json('/path/to/Api/')

    with io.open(file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(sample_rate_hertz=8000,language_code='en-US')

    operation = client.long_running_recognize(config, audio)
    response = operation.result(timeout=90)

    for result in response.results:
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
    decode_text(result.alternatives[0].transcript)
        
def decode_text(text):
    result = [x.strip() for x in text.split('.')]
    print(len(result))
    

app = Flask(__name__)
app.secret_key = "Secret_Key"

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return redirect(url_for('message'))
    return "<a href='/create_session'>login</a>"

@app.route('/create_session', methods = ['GET','POST'])
def create_session():
    if request.method == 'POST':
        #service = session['service']
        service.set_default_headers({'x-watson-learning-opt-out': "true"})
        response = service.create_session(
            assistant_id = assistant_id
            ).get_result()
        print(json.dumps(response, indent=2))
        
        session['username'] = request.form['username']
        session['session_id'] = response["session_id"]
        return redirect(url_for('message'))
    
    return '<form action = "" method = "post"><p><input type = text name = "username"/></p><p><input type = "submit" value = "Login"/></p></form>'

@app.route('/delete_session')
def delete_session():
    response = service.delete_session(
        assistant_id = assistant_id,
        session_id = session['session_id']
        ).get_result()
    session.pop('username', None)
    return "Session deleted"

@app.route('/message', methods = ['GET', 'POST'])
def message():
    if request.method == 'POST':
        print(request.form['emotion'])
        response = service.message(
            assistant_id = assistant_id,
            session_id = session['session_id'],
            input={
                'message_type': 'text',
                'text': request.form['message'] + "," + request.form['emotion']
                }
            ).get_result()
        
        print(response)
        
        return '<form action="" method="post"><h1>' + response["output"]['generic'][0]['text'] + '</h1><input type = text name = "message"/><br><input type="radio" name="emotion" value="anger"> Anger<br><input type="radio" name="emotion" value="noanger"> NoAnger<br><input type = "submit" value = "Send"/></form>'
    return '<form action="" method="post"><input type = text name = "message"/><br><input type="radio" name="emotion" value="anger"> Anger<br><input type="radio" name="emotion" value="noanger"> NoAnger<br><input type = "submit" value = "Send"/></form>'


service = init_watson(version, iam_apikey, url)

if __name__ == "__main__":
    app.run()    

