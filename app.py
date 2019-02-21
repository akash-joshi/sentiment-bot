from flask import Flask,render_template,request
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route("/voice-checker",methods=["POST","OPTIONS"])
def secr():
    a=request.files.get('data')
    fname=request.form.get('fname')
    return (""+fname)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

