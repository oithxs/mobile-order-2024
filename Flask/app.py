from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return "Welcome to Flask!!!"

@app.route('/top')
def top():
    return render_template("/user/top.html")

@app.route('/order')
def order():
    return render_template("/user/order.html")

@app.route('/result',methods=['GET'])
def result():
    return render_template("/user/result.html")

@app.route('/history')
def history():
    return render_template("/user/history.html")

@app.route('/admin')
def admin():
    return render_template("/admin/manage.html")