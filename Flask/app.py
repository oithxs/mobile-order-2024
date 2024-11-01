from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
true = 1

@app.route('/',methods=['GET'])
def home():
    return "Welcome to Flask!!!"

#トップページ
@app.route('/top')
def top():
    return render_template("/user/top.html")

#お客さんが注文するページ
@app.route('/order')
def order():
    return render_template("/user/order.html")

#注文確認ページ
@app.route('/confirm',methods=['GET','POST'])
def confirm():
    return render_template("/user/confirm.html")

#注文完了のページ
@app.route('/result',methods=['GET','POST'])
def result():
    return render_template("/user/result.html")

#注文履歴のページ
@app.route('/history',methods=['GET'])
def history():
    history_data = {
        "nickname": "Mr.Frankfurt",
        "number": 3,
        "time": "14:10",
        "status": "Receptable",
        "ketchup": true,
        "mustard": true
    }
    return render_template("/user/history.html", history_data = history_data)

#エラーページ
@app.route('/error')
def error():
    return render_template("/user/error.html")

#/adminの閲覧ページ
@app.route('/admin')
def admin():
    return render_template("/admin/top.html")

#/adminのシステムメッセージのページ
@app.route('/admin/msg')
def system_message():
    return render_template("/admin/message.html")

#レイアウト確認ページ
@app.route('/layout')
def layout():
    return render_template("/layout_view.html")