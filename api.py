#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json,urllib.request, urllib.parse,configparser
from flask import Flask, request, jsonify


app = Flask(__name__)
#日本語文字化け対応
app.config['JSON_AS_ASCII'] = False

# root
# HelloWorld
@app.route('/', methods=['GET'])
def index():
    return 'Hello World'

# GET通信
# 固定のJSONファイルを返却する
@app.route('/mall-item/api', methods=['GET'])
def get_item_controller():
    # get request data form dialogflow post body
    req = request.get_json(silent=True, force=True)
    # log
    print("Request:")
    print(json.dumps(req, indent=4))
    # read response json file (test)
    res = read_model()
    # make response json and return
    return makeWebFookResult(res)


# POST
# 外部通信をしてデータを取得後に返却をする
@app.route('/mall-item/api', methods=['POST'])
def post_item_controller():
    # get request data form dialogflow post body
    req = request.get_json(silent=True, force=True)
    # log
    print("Request:")
    print(json.dumps(req, indent=4))

    # make url parameter
    p = urllib.parse.urlencode(set_param())
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?" + p
    print("URL:")
    print(url)
    with urllib.request.urlopen(url) as res:
        html = res.read().decode("utf-8")

    #jsonデータ取得
    json_data = json.loads(html)
    print("Data Size : ")
    print(len(json_data['Items']))
    # ランキング1番の商品のみ取り出す
    for item in json_data['Items']:
        if item['Item']['rank'] == 1:
            item_name = item['Item']['itemName']
            print(item['Item']['itemName'])

    # 会話文の作成
    speech = make_speech_sentence(item_name)
    # 会話文を含む返却用のJSONを作成
    res = create_res_json(speech, speech)
    # make response json and return
    return makeWebFookResult(res)


# 外部通信時のリクエストパラメータ
# ※固定のパラメータは外部ファイルから読み込み
def set_param():
    inifile = configparser.ConfigParser()
    inifile.read('./config.ini', 'UTF-8')
    app_id = inifile.get('settings', 'app_id')
    p = {"applicationId": app_id}
    return p

# 会話文の作成
def make_speech_sentence(item_name):
    return "現在のランキング一番の商品は、" + item_name + " です。"

# 回答用のJSON作成
def create_res_json(speech, name):
    d = {"speech": speech,"displayText": name,"source": "dialogflow-mall-item-search"}
    return d

# 固定のJSONファイル読み込み
def read_model():
    try:
        with open('response.json', 'r') as f:
            return json.load(f)
    except IOError as e:
        print(e)
        return None

# DialogFlowへの返却
def makeWebFookResult(data):
    return jsonify(data)

# Main
if __name__ == '__main__':
    app.run(debug=True)
