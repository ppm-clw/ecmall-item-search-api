# ECモール（楽天）の商品ランキングを教えてくれるアプリ

## index
商品ランキングAPIを利用して商品情報が取得できるアプリです。
Flask使ったDialogFlowのFulfillment(WebFook)のサンプルです。

## 使い方

### 1. Flaskインストール
Flaskで動作するため、以下のコマンドでFlaskをインストールする。
`# pip install Flask`

### 2. APP-IDの設定
「config.ini」というファイル名で以下の内容を記述する。
※楽天アプリIDなどは以下のファイルに記載してください。

* config.ini
```
[settings]
app_id : xxxxxxxx ←楽天アプリID
```

### サーバ起動

`# python api.py`

### GETのテスト
ブラウザから以下にアクセスをして商品情報のJSONが表示されれば成功.
`http://localhost:5000/mall-item/api`
