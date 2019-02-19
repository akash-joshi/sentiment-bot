from flask import Flask,render_template
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

