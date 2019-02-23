from flask import (Flask,request,render_template)
from flask_cors import CORS,cross_origin
'''import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import librosa
import wave as wa
import os
import tensorflow as tf
from keras.models import load_model
global graph,model,emotion'''

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#each time the server starts is equal to a new session on call

@app.route('/')
def main():
    return render_template('index.html')

#graph = tf.get_default_graph()
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
	
#model = load_model('server/rnn_mfcc_model_ver_1_CPU.h5')

@app.route("/voice-checker",methods=["POST","OPTIONS"])
@cross_origin()
def secr():
    #print(request.data)
    global count
    a=request.files.get('data')
    fname=request.form.get('fname')
  #  files.append(fname)
    a.save(fname)
    '''x=toMfcc(fname)
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
''''''
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
    app.run(debug=True, use_reloader=True)    