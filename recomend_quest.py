from flask import Flask, session, redirect, url_for, escape, request, render_template
import csv

def init_csv_file():
    csvfile = 'dialogs.txt'
    csv_reader = csv.resder(csvfile)

app = Flask(__name__)

"""
POST param=quest(string)
takes in intent of previous question from watson
watson provides intent, entites, response. Use that intent here.
"""


@app.route('/index', methods=['GET','POST'])
def message():
    if (request.method == 'POST'):
        quest = request.form['message']
        response = ""

        with open('dialogs.txt') as csv_file:
            csv_reader = csv.reader(csv_file)
            #questnos = sum(1 for row in csv_reader)
            questnos = 11
            idx = 0
            #rows = list(csv_reader)
            for row in csv_reader:
                if(row[0] == quest):
                    print("true")
                    if(idx == questnos-1):
                        response = ""
                    elif idx == questnos-2:
                        response = next(csv_reader)[1]
                    else :
                        response = next(csv_reader)[1] + ", <br>" + next(csv_reader)[1]
                    break
                idx += 1
                        
        print(response)
        return '<form action="" method="post"> <input id="message" name="message" type=text></input> <input type = "submit" value = "Login"/> <h5>Tips:</h5><p id="tips">' + response + '</p></form>'
        
    return """
        <form action="" method="post">
            <input id="message" name="message" type=text></input>
            <input type = "submit" value = "Login"/>
            <h5>Tips:</h5>
            <p id="tips">None</p>
        </form>
    """

if __name__ == "__main__":
    app.run()
