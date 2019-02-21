from flask import Flask,render_template,request
from flask_cors import CORS,cross_origin
from datetime import datetime
import librosa
import pandas as pd
import numpy as np
import os
app = Flask(__name__)
CORS(app)

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route("/voice-checker",methods=["POST","OPTIONS"])
def secr():
    a=request.files.get('data')
    fname=request.form.get('fname')
    a.save(fname)
    x=toMfcc(fname)
    res=prePro(x)
    delFile(fname)
    print(res)
    return (res.tostring())


def delFile(f):
 if os.path.exists(f):
   os.remove(f)
 else:
   print("The file does not exist") 


def toMfcc(file):
   X, sample_rate = librosa.load(file, res_type='kaiser_fast')
   mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
   return mfccs


def prePro(x):
    res= pd.DataFrame(data=x) 
    res = res.stack().to_frame().T
    res= np.expand_dims(res, axis=2)
    return res


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

