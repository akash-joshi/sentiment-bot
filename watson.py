import watson_developer_cloud
import json
from flask import Flask, session, redirect, url_for, escape, request


def init_watson(version, iam_apikey, url):
    service = watson_developer_cloud.AssistantV2(
        version = version,
        iam_apikey = iam_apikey,
        url = url
        )
    return service

app = Flask(__name__)
app.secret_key = "ssup bro"

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return redirect(url_for('message'))
    return "<a href='/create_session'>login</a>"

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '<form action = "" method = "post"><p><input type = text name = "username"/></p><p><input type = "submit" value = "Login"/></p></form>'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


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
        response = service.message(
            assistant_id = assistant_id,
            session_id = session['session_id'],
            input={
                'message_type': 'text',
                'text': request.form['message']
                }
            ).get_result()
        print(response)
        return '<form action="" method="post"><h1>' + response + '</h1><input type = text name = "message"/><input type = "submit" value = "Send"/></form>'
    return '<form action="" method="post"><input type = text name = "message"/><input type = "submit" value = "Send"/></form>'

version = '2018-11-08'
iam_apikey = 'wQ_1OrWKz-2ZTx4rI4AzRxOsuiTAj2F4E5vTHLMZ_r0r'
url = 'https://gateway-lon.watsonplatform.net/assistant/api'
assistant_id = '8565e9a4-f45f-43b3-b87e-e54c4dbfa754'

#service = init_watson(version, iam_apikey, url)
#session_id = create_session(service, assistant_id)
#print (session_id)
#message(service, assistant_id, session_id, 'text', 'hello')
#delete_session(service, assistant_id, session_id)

service = init_watson(version, iam_apikey, url)
if __name__ == "__main__":
    app.run()    

