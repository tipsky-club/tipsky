from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    heim = request.args.get('heim')
    gast = request.args.get('gast')

    res=[heim, gast]
    res_a = {"a": res, "b": res}
    return json.dumps(res_a)