from flask import (Flask,request)
from flask_cors import CORS
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import librosa
import wave as wa
import os
import tensorflow as tf
from keras.models import load_model
global graph,model
graph = tf.get_default_graph()
files=[]
app = Flask(__name__)
CORS(app)

def toMfcc(file):
   X, sample_rate = librosa.load(file, res_type='kaiser_fast')
   mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
   return mfccs

def prePro(x):
    res= pd.DataFrame(data=x) 
    res = res.stack().to_frame().T
    res= np.expand_dims(res, axis=2)
    return res
	
model = load_model('rnn_mfcc_model_ver_1.h5')
@app.route("/voice-checker",methods=["POST"])
def secr():
    #print(request.data)
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
    print(fresult)
    os.remove(fname)
    val=fresult[0]
    return("Emotion:"+str(val))
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
		
		
if __name__ == "__main__":
    app.run(port='8000')    