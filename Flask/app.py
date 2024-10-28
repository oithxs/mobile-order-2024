from flask import Flask, render_template, redirect, url_for,request

app = Flask(__name__)

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

    order_data = {
        "nickname": "ドッグフランク",
        "isOrderLeft": True
    }

    if(order_data['isOrderLeft']):
        return render_template("/user/order.html", order_data=order_data)
    else:
        return redirect(url_for('error'))

#注文確認ページ
@app.route('/confirm',methods=['POST'])
def confirm():
    order_data = request.form
    return render_template("/user/confirm.html",order_data=order_data)

#注文完了のページ
@app.route('/result',methods=['POST'])
def result():
    order_data = request.form #このorder_dataを使ってDBに保存する
    return render_template("/user/result.html")

#注文履歴のページ
@app.route('/history')
def history():
    return render_template("/user/history.html")

#エラーページ
@app.route('/error')
def error():
    return render_template("/user/error.html")

#/adminの閲覧ページ
@app.route('/admin')
def admin():
    admin_data = [
        {"ニックネーム":"山田", "本数":5, "ケチャップ":True, "マスタード":True, "予定時刻":"15:00"},
        {"ニックネーム":"tom", "本数":15, "ケチャップ":False, "マスタード":True, "予定時刻":None},
        {"ニックネーム":"まいける", "本数":6, "ケチャップ":True, "マスタード":False, "予定時刻":"9:15"},
    ]
    return render_template("/admin/top.html", data=admin_data)

@app.route('/delete', methods=['POST'])
def delete():
    name = request.form['ニックネーム']
    return f"Delete: {name}"

#/adminのシステムメッセージのページ
@app.route('/admin/msg')
def system_message():
    return render_template("/admin/message.html")

#レイアウト確認ページ
@app.route('/layout')
def layout():
    return render_template("/layout_view.html")
    
