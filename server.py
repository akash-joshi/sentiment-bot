from flask import (Flask,request)
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/secr",methods=["POST"])
def secr():
    print(request.get_json(force=True))
    return("lol")