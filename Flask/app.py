from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import sys
from datetime import datetime as dt
from datetime import timedelta
import random
import json

# envファイルを読み込む
load_dotenv()
user = os.environ["MYSQL_USER"]
password = os.environ["MYSQL_PASSWORD"]
db = os.environ["MYSQL_DATABASE"]
host = os.environ["MYSQL_HOST"]

app = Flask(__name__)

app.secret_key = os.urandom(24)

db_uri = f"mysql+pymysql://{user}:{password}@{host}/{db}?charset=utf8"
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
db = SQLAlchemy(app)


# ---------------------------------------------------------------------------
# DB生成処理
class Reservation(db.Model):
    __tablename__ = "reservation"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text())
    number = db.Column(db.Integer)
    ketchup = db.Column(db.Boolean)
    mustard = db.Column(db.Boolean)
    reservationTime = db.Column(db.DateTime)


class Nickname(db.Model):
    __tablename__ = "nickname"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text())
    status = db.Column(db.Boolean)


class Received(db.Model):
    __tablename__ = "received"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text())
    number = db.Column(db.Integer)

class StoreStatus(db.Model):
    __tablename__ = "store_status"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_open = db.Column(db.Boolean, default=False)  # 初期状態は営業中

# ---------------------------------------------------------------------------
# adminの削除処理
def destroy(id):
    message = "Destroy SQLAlchemy"
    # データ削除
    reservation = Reservation.query.get(id)
    db.session.delete(reservation)
    db.session.commit()

#----------------------------------------------------------------------------
## 追加内容
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer,Boolean,DateTime,String,Column
from sqlalchemy.orm import Session

engine = create_engine(db_uri)
Base = declarative_base()

class Reservation2(Base):
    __tablename__ = 'reservation'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(255))
    number = Column(Integer)
    ketchup = Column(Boolean)
    mustard = Column(Boolean)
    reservationTime = Column(DateTime)

# user side True
# 使える：True
# 使用済み（もう使えない）：False
def update_nickname_status1(session, id: int, new_status: bool):
    nickname_record = session.query.get(id)
    if nickname_record:
        nickname_record.status = new_status
        db.session.commit()


def update_nickname_status2(session, nickName: str, new_status: bool):
    nickname_record = session.query.all()
    for oneNickName in nickname_record:
        if oneNickName.name == nickName or '*'+oneNickName.name == nickName:
            update_nickname_status1(session, oneNickName.id, new_status)
            return True
    return False


def addReceived(name: str, number: int):
    new_received = Received(name=name, number=number)
    db.session.add(new_received)
    db.session.commit()

def is_store_open():
    store_status = StoreStatus.query.first()
    return store_status.is_open


"""ここはデータベースに何を追加するプログラム"""


# ユーザが予約したデータを登録する
def add_reservation(
    name: str, number: int, ketchup: bool, mustard: bool, now_time: dt
):
    new_reservation = Reservation(
        name=name,
        number=number,
        ketchup=ketchup,
        mustard=mustard,
        reservationTime=now_time,
    )
    db.session.add(new_reservation)
    db.session.commit()


"""
adminの一覧画面からの取得
"""

def get_reservations():
    #reservations = Reservation.query.all()
    reservations =  Reservation.query.order_by(Reservation.reservationTime).all()
    return reservations


# ---------------------------------------------------------------------------
# /adminの編集処理


def update_reservation_by_id(
    id: int, name: str, number: int, ketchup: bool, mustard: bool, now_time: dt
):
    reservation = Reservation.query.get(id)

    if reservation:
        if name is not None:
            reservation.name = name
        if number is not None:
            reservation.number = number
        if ketchup is not None:
            reservation.ketchup = ketchup
        if mustard is not None:
            reservation.mustard = mustard
        if now_time is not None:
            reservation.reservationTime = now_time

        db.session.commit()


# ---------------------------------------------------------------------------
# デバッグ用プログラム


def getOrderHistory(id: int):
    order = Reservation.query.get(id)
    name = order.name
    number = order.number
    ketchup = order.ketchup
    mustard = order.mustard
    reservationTime = order.reservationTime
    return name, number, ketchup, mustard, reservationTime


def login_required(func):
    import functools

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("username") is None:

            return redirect(url_for("login"))  ##ここ

        else:
            return func(*args, **kwargs)

    return wrapper


"""
#################################################ルーティング部#################################################
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
"""


# /の場合の遷移
@app.route("/")
def index():
    return redirect("/top")


# トップページ
@app.route("/top", methods=["GET"])
def top_user():
    return render_template("user/top.html")


# お客さんが注文するページ
@app.route("/order", methods=["GET"])
def order():
    if(not is_store_open()):
        return render_template("/user/error.html")
    else:
        return render_template("user/order.html",)


# 注文確認のページ
@app.route("/confirm", methods=["POST"])
def confirm():
    return render_template("user/confirm.html",order_data=request.form)

#注文処理のページ
@app.route('/processing_order',methods=['POST'])
def processing_order():
    if(request.form.get('isNicknameRegistered') == "true"):
        return redirect(url_for('result', nickname=request.form['nickname']))
    else:
        # ニックネームをランダムで取り出す(import randomの記述お願いします)
        nicknameList = Nickname.query.all()
        nicknameList = [name for name in nicknameList if name.status==True]
        nickname = nicknameList[random.randint(0,len(nicknameList)-1)]
        nickname.status = bool(False)
        db.session.commit()

        order_data = request.form.to_dict() # formデータを受け取る

        #order_dataの加工
        ketchup = False
        mustard = False
        reservationTime = dt.now()
        if order_data['ketchup'] == 'true':
            ketchup = True
        if order_data['mustard'] == 'true':
            mustard = True
        if order_data['reservationTime'] != 'none':
            today = dt.today()
            reservationTime = dt.strptime(today.strftime('%Y-%m-%d')+" "+order_data['reservationTime'], "%Y-%m-%d %H:%M")

        add_reservation(nickname.name, int(order_data['count']), ketchup, mustard, reservationTime)

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
        order_DB = Reservation.query.all()
        for nickname in nicknames:
            for order in order_DB:
                if nickname == order.name or '*'+nickname == order.name:
                    history_data.append(order) # データベースからニックネームをキーとして履歴データを取る
        return render_template("/user/history.html", history_data = history_data)

# エラーページ
@app.route("/error", methods=["GET"])
def error():
    return render_template("user/error.html")

@app.route("/admin/View")
@login_required
def view():
    try:
        reservations = get_reservations()
        return render_template("/admin/top.html", reservations=reservations)
    except:
        return render_template("/admin/message.html", message="DB Failed", type="error")


@app.route("/admin/delete/<int:id>")
@login_required
def delete(id):
    try:
        # データ削除関数 or メソッド
        name, number, ketchup, mustard, reservationTime = getOrderHistory(id)
        # これはたぶんいるけど T F のどちらにするべき
        update_nickname_status2(Nickname, name, new_status=True)
        destroy(id)
        addReceived(name,int(number))
        return redirect(url_for("view",message="DeleteSuccess",type="message"))
    except:
        return redirect(url_for("view",message="DeleteFailed",type="error"))



@app.route("/admin/edit/<int:id>", methods=["POST"])
@login_required
def edit(id):
    try:
        # 全部のデータが来る想定、
        form_data = request.form.to_dict()
        form_data["ketchup"] = True if "ketchup" in form_data else False
        form_data["mustard"] = True if "mustard" in form_data else False
        update_reservation_by_id(
            id,
            str(form_data["name"]),
            int(form_data["number"]),
            bool(form_data["ketchup"]),
            bool(form_data["mustard"]),
            # dt.strptime(form_data["reservationTime"], "%Y-%m-%d %H:%M:%S"),
            form_data["reservationTime"],
        )

        return redirect(url_for("view",message="EditSuccess",type="message"))
    except:
        return redirect(url_for("view",message="EditFailed",type="error"))

@app.route("/admin/open", methods=["GET"])
@login_required
def open_store_route():
    try:
        store_status = StoreStatus.query.first()
        store_status.is_open = not store_status.is_open
        db.session.commit()
        if store_status.is_open:
            return redirect(url_for("view",message="OPEN" ,type="message"))
        else:
            return redirect(url_for("view",message="CLOSE",type="message"))
    except:
        return redirect(url_for("view",message="ERROR" ,type="error"))


@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == os.environ.get("USER") and password == os.environ.get(
            "PASSWORD"
        ):
            session["username"] = username

            return redirect("/admin/View")

        else:
            return render_template("/admin/login.html")
    else:
        return render_template("/admin/login.html")

if __name__ == '__main__':
    # app.debug = False
    # app.run(host="0.0.0.0",port=5000)
    app.run()
