from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    heim = request.args.get('heim')
    gast = request.args.get('gast')
    return 'Es spielt ' + heim + " gegen " + gast