from flask import Flask,render_template,request
from flask_cors import CORS,cross_origin
from datetime import datetime
import librosa
import pandas as pd
import numpy as np
import os
from keras.models import load_model
import tensorflow as tf
app = Flask(__name__)
CORS(app)
global graph,model,emotion
app.config['UPLOAD_FOLDER'] = 'tmp/'

model = load_model('model/rnn_mfcc_model_ver_1_CPU.h5')

graph = tf.get_default_graph()
files=[]

emotion=["neutral"," calm","happy","sad","angry","fearful","disgust","surprised"]
count=0


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route("/voice-checker",methods=["POST","OPTIONS"])
def secr():
    mypath=os.getcwd()+'/tmp/'
    if not os.path.isdir(mypath):
	      os.mkdir(mypath)
    a=request.files.get('data')
    fname=request.form.get('fname')
    a.save(os.path.join(app.config['UPLOAD_FOLDER'],fname))
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],fname)):
      print(""+fname)
      x=toMfcc(fname)
      res=prePro(x)
    print("Before predict")
    with graph.as_default():
      result=model.predict(res)
    print("After predict")
    fresult=result.argmax(axis=1)
    val=fresult[0]
    em=emotion_norm(val)
    delFile(fname)
  #  print(res)
    print(emotion[em])
    return ("Emotion:"+emotion[em])



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


def delFile(f):
 if os.path.exists(f):
   os.remove(f)
 else:
   print("The file does not exist") 


def toMfcc(file):
   X, sample_rate = librosa.load(os.path.join(app.config['UPLOAD_FOLDER'],file), res_type='kaiser_fast')
   mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
   return mfccs


def prePro(x):
    res= pd.DataFrame(data=x) 
    res = res.stack().to_frame().T
    res= np.expand_dims(res, axis=2)
    return res


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

