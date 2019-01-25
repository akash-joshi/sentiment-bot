from flask import (Flask,request)
from flask_cors import CORS
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
#import librosa
#from keras.models import load_model

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
	
#model = load_model('rnn_mfcc_model_ver_1.h5')

@app.route("/voice-checker",methods=["POST"])
def secr():
    #f = open('file.wav', 'wb')
    #f.write(request.data)
    #f.close()
    #print(request.data)
    a=request.files.get('data')
    a.save('a.wav' )
    #print(a)
    return("server_response")
'''
    #audio_file=request.files
    x=toMfcc(a)
    res=prePro(x)
    print(res)
    result=model.predict(res)
    result=result.argmax(axis=1)
    return(result)
'''

if __name__ == "__main__":
    app.run(port='8000')    