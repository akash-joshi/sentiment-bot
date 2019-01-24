from flask import (Flask,request)
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/voice-checker",methods=["POST"])
def secr():
    print(request.form.get('fname'))
    print(request.files)
    return("server data")

if __name__ == "__main__":
    app.run(port='8000')    