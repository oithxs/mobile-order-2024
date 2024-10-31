from flask import Flask, render_template, request, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import functools
import os
from dotenv import load_dotenv
from datetime import datetime as dt
import random

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


# ---------------------------------------------------------------------------
# adminの削除処理
def destroy(id):
    message = "Destroy SQLAlchemy"

    # データ削除
    reservation = Reservation.query.get(id)
    db.session.delete(reservation)
    db.session.commit()

    return "ok"


# ---------------------------------------------------------------------------
# /adminと/userの取得処理
from datetime import datetime


# user side
def get_nicknames():
    nicknames = Nickname.query.all()
    return nicknames


# user side True
# 使える：True
# 使用済み（もう使えない）：False
def update_nickname_status1(session, id: int, new_status: bool):
    nickname_record = session.query.get(id)
    if nickname_record:
        nickname_record.status = new_status
        db.session.commit()
    else:
        print("Nickname not found")


def update_nickname_status2(session, nickName: str, new_status: bool):
    nickname_record = session.query.all()
    for oneNickName in nickname_record:
        if oneNickName.name == nickName:
            update_nickname_status1(session, oneNickName.id, new_status)
            return True
    print("Nickname not found")
    return False


def addReceived(name: str, number: int):
    new_received = Received(name=name, number=number)
    db.session.add(new_received)
    db.session.commit()


"""ここはデータベースに何を追加するプログラム"""


# ユーザが予約したデータを登録する
def add_reservation(
    name: str, number: int, ketchup: bool, mustard: bool, now_time: datetime
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
    reservations = Reservation.query.all()
    print(reservations)
    return reservations


# ---------------------------------------------------------------------------
# /adminの編集処理


def update_reservation_by_id(
    id: int, name: str, number: int, ketchup: bool, mustard: bool, now_time: datetime
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
            reservation.ard = mustard
        if now_time is not None:
            reservation.time = now_time

        db.session.commit()

    else:
        print("Reservation not found.")


# ---------------------------------------------------------------------------
# デバッグ用プログラム
def show_nickname(data):
    for dt in data:
        print(f"{dt.id} {dt.name} {dt.status}")


def show_reservation(data):
    for dt in data:
        print(
            f"{dt.id} {dt.name} {dt.number} {dt.ketchup} {dt.mustard} {dt.reservationTime}"
        )


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
    # ニックネームをランダムで取り出す(import randomの記述お願いします)
    while True:
        nickname = Nickname.query.get(
            random.randint(1, 100)
        )  ##(1,100)はニックネームの数に合わせる
        if nickname.status == True:
            break
    return render_template("user/order.html", nickname=nickname)


# 注文確認のページ
@app.route("/confirm", methods=["GET"])
def confirm():
    return render_template("user/confirm.html")


# 注文完了のページ
@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "GET":
        return render_template("user/result.html")
    if request.method == "POST":
        add_reservation(
            request.form["name"],
            int(request.form["number"]),
            bool(request.form["ketchup"]),
            bool(request.form["mustard"]),
            dt.strptime(request.form["reservationTime"], "%Y-%m-%d %H:%M:%S"),
        )
        nickname = Nickname.query.get(id)
        nickname.status = bool(False)
        db.session.commit()
        return render_template("user/result.html")


# エラーページ
@app.route("/error", methods=["GET"])
def error():
    return render_template("user/error.html")


# 注文履歴のページ
@app.route("/history/<int:id>", methods=["GET"])
def history(id):
    reservation = Reservation.query.get(id)
    return render_template("user/history.html", reservation=reservation)


@app.route("/admin/View")
@login_required
def view():
    try:
        reservations = get_reservations()
        return render_template("/admin/top.html", reservations=reservations)
    except:
        return render_template("/admin/message.html", message="view failed")


@app.route("/admin/delete/<int:id>")
@login_required
def delete(id):
    try:
        # データ削除関数 or メソッド
        # 引数 id
        name, number, ketchup, mustard, reservationTime = getOrderHistory(id)
        destroy(id)
        # これはたぶんいるけど T F のどちらにするべき
        update_nickname_status2(Nickname, name, new_status=True)
<<<<<<< HEAD
        addReceived(name, int(number))
        return redirect(url_for("view", message="delete success"))
    except:
        return redirect(url_for("view", message="delete failed"))
=======
        addReceived(name,int(number))
        return redirect(url_for("view",message="DeleteSuccess",type="message"))
    except:
        return redirect(url_for("view",message="DeleteFailed",type="error"))
>>>>>>> 0bb1d8a8334eb8eefd9f60a3fd4c8cfaead903f4


@app.route("/admin/edit/<int:id>", methods=["POST"])
@login_required
def edit(id):
    try:
        # 全部のデータが来る想定、
        if request.method == "POST":
            form_data = request.form.to_dict()

            update_reservation_by_id(
                id,
                str(form_data["name"]),
                int(form_data["number"]),
                bool(form_data["ketchup"]),
                bool(form_data["mustard"]),
                dt.strptime(form_data["reservationTime"], "%Y-%m-%d %H:%M:%S"),
            )
<<<<<<< HEAD
            return redirect(url_for("view", message="edit success"))
=======
            return redirect(url_for("view",message="EditSuccess",type="message"))

>>>>>>> 0bb1d8a8334eb8eefd9f60a3fd4c8cfaead903f4

        else:
            return "<h1>Not Found</h1><p>メソッド違い</p>"
    except:
<<<<<<< HEAD
        return redirect(url_for("view", message="edit failed"))
=======
        return redirect(url_for("view",message="EditFailed",type="error"))
>>>>>>> 0bb1d8a8334eb8eefd9f60a3fd4c8cfaead903f4


# @app.route('/admin/system/message')
# @login_required
# def message():
#     return render_template("/admin/message.html")


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


if __name__ == "__main__":
    app.debug = True
    app.run()
