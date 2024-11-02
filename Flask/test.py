
# Flaskで利用するパッケージをインポートする
from flask import Flask, jsonify

# アプリケーションオブジェクトを生成する
app = Flask(__name__)

# エンドポイントを作る(http://host/hello にリクエストするとJSONが表示される)
@app.route("/hello")
def hello():
    return jsonify({
        "message": "Hello World!"
    })
