#from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for,request
import json, random

app = Flask(__name__)

order_DB = [ # 仮の注文DB
            { # ダミーデータ
                "number": 1,
                "time": "11:30",
                "nickname": "Mr.Frankfurt",
                "status": "Received",
                "count": 4,
                "ketchup": True,
                "mustard": True
            }
]
nickname_DB = ["ドッグフランク", "フランクキング", "フルート",
            "ドッグキング", "フランククイーン", "枚方太郎", "京橋花子"] # 仮のニックネームのDB

isOrderLeft = True # 注文可能かどうか (Falseの場合にエラーページに飛ぶようにする)

@app.route('/',methods=['GET'])
def home():
    return redirect(url_for('top')) # topページに強制リダイレクト

#トップページ
@app.route('/top')
def top():
    return render_template("/user/top.html")

#お客さんが注文するページ
@app.route('/order')
def order():

    if(isOrderLeft):
        return render_template("/user/order.html")
    else:
        return redirect(url_for('error'))

#注文確認ページ
@app.route('/confirm',methods=['POST'])
def confirm():
    return render_template("/user/confirm.html",order_data=request.form)

#注文処理のページ
@app.route('/processing_order',methods=['POST'])
def processing_order():
    if(request.form.get('isNicknameRegistered') == "true"):
        return redirect(url_for('result', nickname = request.form['nickname']))
    else:
        nickname = random.choice(nickname_DB) # ニックネームをニックネームDBから取得する
        nickname_DB.remove(nickname)

        order_data = request.form.to_dict() # formデータを受け取る

        #order_dataの加工
        order_data['nickname'] = nickname
        order_data['status'] = "Receptable"
        order_data['count'] = int(order_data['count'])
        if order_data['ketchup'] == 'true':
            order_data['ketchup'] = True
        else:
            order_data['ketchup'] = False
        if order_data['mustard'] == 'true':
            order_data['mustard'] = True
        else:
            order_data['mustard'] = False
        if order_data['reservationTime'] == 'none':
            order_data['reservationTime'] = None

        order_DB.append(order_data) # order_dataをDBに保存（ここではorder_DBに保存している）

        return render_template("/user/processing_order.html",nickname = nickname)

#注文完了のページ
@app.route('/result',methods=['GET'])
def result():

    nickname = request.args.get('nickname')
    if nickname == None:
        nickname = ""
    return render_template("/user/result.html", nickname = nickname)

#注文履歴のページ
@app.route('/history',methods=['GET','POST'])
def history():
    if request.method == 'GET':
        return render_template("user/loading.html") # このページでローカルストレージの内容を取り出す
    else:
        nicknames = json.loads(request.form.get('nicknames')) # ニックネームの文字列のリスト

        history_data = [] # 履歴データ

        for nickname in nicknames:
            for order in order_DB:
                if nickname in order.values():
                    history_data.append(order) # データベースからニックネームをキーとして履歴データを取る

        return render_template("/user/history.html", history_data = history_data)

#エラーページ
@app.route('/error')
def error():
    return render_template("/user/error.html")

#/adminの閲覧ページ
@app.route('/admin')
def admin():
    admin_data = [
        {"ニックネーム":"山田あああ", "本数":5, "ケチャップ":True, "マスタード":True, "予定時刻":"15:00"},
        {"ニックネーム":"tom", "本数":15, "ケチャップ":False, "マスタード":True, "予定時刻":None},
        {"ニックネーム":"まいける", "本数":6, "ケチャップ":True, "マスタード":False, "予定時刻":"9:15"},
    ]
    return render_template("/admin/top.html", data=admin_data)

@app.route('/delete', methods=['POST'])
def delete():
    name = request.form['ニックネーム']
    return f"Delete: {name}"
