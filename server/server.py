from flask import (Flask,request)
from flask_cors import CORS
import pandas as pd
import numpy as np

import librosa
from keras.models import load_model

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
    print(request.form.get('fname'))
    print(request.files)
	audio_file=request.files
	x=toMfcc(audio_file)
	res=prePro(x)
	result=model.predict(res)
	result=result.argmax(axis=1)
    return(result)

if __name__ == "__main__":
    app.run(port='8000')    