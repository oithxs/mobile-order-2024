from flask import Flask, render_template, request
from admin_view import admin_view
import os

app = Flask(__name__)

app.register_blueprint(admin_view,url_prefix="/admin")
app.secret_key = os.urandom(24)


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
@app.route('/history')
def history():
    return render_template("/user/history.html")

#エラーページ
@app.route('/error')
def error():
    return render_template("/user/error.html")

#レイアウト確認ページ
@app.route('/layout')
def layout():
    return render_template("/layout_view.html")
