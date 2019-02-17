from flask import (Flask,request,render_template)
from flask_cors import CORS
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import librosa
import wave as wa
import os
import tensorflow as tf
from keras.models import load_model
global graph,model,emotion

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
'''
#each time the server starts is equal to a new session on call

@app.route('/')
def main():
    return render_template('index.html')
'''
graph = tf.get_default_graph()
files=[]


emotion=["neutral"," calm","happy","sad","angry","fearful","disgust","surprised"]
count=0
def toMfcc(file):
   X, sample_rate = librosa.load(file, res_type='kaiser_fast')
   mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
   return mfccs

def prePro(x):
    res= pd.DataFrame(data=x) 
    res = res.stack().to_frame().T
    res= np.expand_dims(res, axis=2)
    return res
	
model = load_model('server/rnn_mfcc_model_ver_1_CPU.h5')

def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route("/voice-checker",methods=["POST","OPTIONS"])
@crossdomain(origin='*')
def secr():
    #print(request.data)
    global count
    a=request.files.get('data')
    fname=request.form.get('fname')
  #  files.append(fname)
    a.save(fname)
    x=toMfcc(fname)
    res=prePro(x)
  #  print(res)
    with graph.as_default():
      result=model.predict(res)
    fresult=result.argmax(axis=1)
   # print(a)
    #x=wa.open(io.BytesIO(z),mode='rb')
   # print(fresult)
    os.remove(fname)
    val=fresult[0]
    em=emotion_norm(val)
 #   print(emotion[val])
    print(emotion[em])
    return("Emotion:"+emotion[em])
'''
    #audio_file=request.files
    x=toMfcc(a)s
    res=prePro(x)
    print(res)
    ressult=model.predict(res)
    result=result.argmax(axis=1)
    return(result)
'''


def deleteTempAudioFile(f):#use this when we can detect connection is closed
    for file in f:
	    os.remove(file)
emo=0		
def emotion_norm(v):
    reduced_emo=emotion_red(v)
    global emo
    if reduced_emo==2:
        emo+=6
        if emo<-5:
          emo+=3
        if emo<-15:
          emo+=10		
    elif reduced_emo==0:
        emo-=2
    else:
        emo-=4
	   
    print(emo)   
    if emo>=10:
       return 4
    elif emo<0:
       return 2
    else:
       return 0

def emotion_red(v):
    if v==4 or v==5 or v==6:
       return 2
    elif v==0 or v==1 or v==3:
       return 0
    else:
       return 1

if __name__ == "__main__":
    app.run()    