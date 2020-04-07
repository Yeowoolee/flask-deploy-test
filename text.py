import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h3>Hi, Heroku</h3>'

if __name__ == '__main__':
    #app.run(debug=True, host='127.0.0.1')
    app.run()
