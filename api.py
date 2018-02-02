#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
#日本語文字化け対応
app.config['JSON_AS_ASCII'] = False

# root
@app.route('/', methods=['GET'])
def index():
    return 'Hello World'

# GET Request
@app.route('/mall-item/api', methods=['POST'])
def post():
    # get request data form dialogflow post body
    req = request.get_json(silent=True, force=True)
    # log
    print("Request:")
    print(json.dumps(req, indent=4))
    # read response json file (test)
    res = read_model()
    # make response json and return
    return makeWebFookResult(res)

# read response json
def read_model():
    try:
        with open('response.json', 'r') as f:
            return json.load(f)
    except IOError as e:
        print(e)
        return None

# make webfook(FulfillMent) Result of Json
def makeWebFookResult(data):
    return jsonify(data)

# Main
if __name__ == '__main__':
    app.run(debug=True)
