from flask import Flask, render_template, request, request, session, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import sys
from datetime import datetime as dt
from datetime import timedelta
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
    

# 焼き時間を環境変数から読み取る
bakingTime = int(os.environ['BAKINGTIME']) # 焼き時間は分

# 現在の時刻を取得する
def nowTime():
    return dt.now()

# バックアップデータの書き込み
def backUpWrite(count :int):
    backUp = open('backUpNum.txt','w')
    backUp.write(str(count))
    backUp.close()
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
        if oneNickName.name == nickName or '*'+oneNickName.name == nickName:
            update_nickname_status1(session, oneNickName.id, new_status)
            return True
    print("Nickname not found")
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
    #reservations = Reservation.query.all()
    reservations =  Reservation.query.order_by(Reservation.reservationTime).all()
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
            reservation.mustard = mustard
        if now_time is not None:
            reservation.reservationTime = now_time

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
    if(not is_store_open()):
        return render_template("/user/error.html")
    else:
        # ニックネームをランダムで取り出す(import randomの記述お願いします)
        nicknameList = Nickname.query.all()
        nicknameList = [name for name in nicknameList if name.status==True]
        nickname = nicknameList[random.randint(0,len(nicknameList)-1)]
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

@app.route("/test", methods=["POST"])
def test():
    form_data = request.form.to_dict()
    form_data["check"] = True if "check" in form_data else False
    form_data["time"] = dt.strptime(form_data["reservationTime"], "%Y-%m-%d %H:%M:%S")
    return form_data
    # return render_template("/admin/message.html", message=form_data)

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



@app.route('/admin/system/message')
def message():
    return render_template("/admin/message.html")


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

# バックアップデータの読み取り
def backUpRead():
    with open('backUpNum.txt','r') as backUp:
        try:
            readData = int(backUp.readline())
        except FileNotFoundError:
            print("BackUpFile is not foud or not data.")
            sys.exit()
        except ValueError:
            print("The data is strange.")
            sys.exit()
        else:
            backUp.close() 
            return readData
        
# バックアップデータ（焼き本数）を取得
bakingNum = backUpRead()
# 更新時刻を取得
newTime = nowTime()

# 現在の時刻に焼き始めなければならないフランクフルトの数を取得する関数
from sqlalchemy import func
def get_frankfurts_to_start_baking():
    current_time = nowTime()
    bake_start_time = current_time + timedelta(minutes=bakingTime)

    cuTime = bake_start_time.strftime('%H:%M')

    print(f"現在チェックした予約データ:{cuTime}")



    print(f"予約:{bake_start_time.hour}時{bake_start_time.minute}分")

    setHour = bake_start_time.hour
    setMinute = bake_start_time.minute

    session = Session(autocommit=False,autoflush=True,bind=engine)


    # 焼き始める必要がある予約の数を取得
    frankfurts_to_start = session.query(func.sum(Reservation2.number)).filter(func.hour(Reservation2.reservationTime)==setHour,func.minute(Reservation2.reservationTime)==setMinute).scalar()
    if(frankfurts_to_start==None):
        return 0
    
    return frankfurts_to_start


#更新システム
import threading
import time
def count():
    global bakingNum
    global newTime
    #時間格納に関する設定を行う

    # 現在焼かなければならない数を取得
    frankfurts_to_start = get_frankfurts_to_start_baking()
    bakingNum += frankfurts_to_start
    # バックアップデータを書き込む
    backUpWrite(bakingNum)
    newTime = nowTime()
    print(f"焼かなければならない数を更新しました: {bakingNum}本")

# 自動更新関数を呼び出すスレッド
def update():
    temp = 0
    while True:
        #print(f"現在時刻:{nowTime()}")
        if(nowTime().minute != temp):
            temp = nowTime().minute
            print("更新中")
            count()
        time.sleep(1) 
            
# 別スレッド起動
update_thread = threading.Thread(target=update, daemon=True)
update_thread.start()


#----------------------------------------------------
# ★今後の拡張用関数
# 予約状況より何分遅延しているかを出力する
def reservationlate(id: int):
    time00 = nowTime()
    reservation11 = Reservation.query.get(id)
    if(reservation11!=None):
        reservationlate  = time00 - reservation11.reservationTime

    if reservation11 is None:
        # 予約されていない/受け取り済み
        return "データがありません。"
    elif(reservationlate.days > 0):
        # 遅延している
        return f"{reservationlate.seconds / 60}分遅延しています。"
    else:
        # 遅延していない
        return "遅延していません。"
#-----------------------------------------------------


#---------------------------------------------------------
## 焼き本数通知システム（ルーティング）
# 焼かなければならない数を確認するページ
@app.route('/bakingCheck')
@login_required
def BakingCheck():
    # 焼かなければならない数を取得
    return render_template("admin/bakingCheck.html")

# 焼かなければならない数をリセットするページ
@app.route('/bakingCountReset')
@login_required
def bakingCountReset():
    global bakingNum
    global newTime
    bakingNum = 0
    newTime = nowTime()
    backUpWrite(bakingNum)
    return "<p>処理中です...</p><script>window.location.href = 'bakingCheck';</script>"

# 情報を取得(JSON形式で返却)
@app.route('/getData')
@login_required
def getData():
    global bakingNum
    global newTime
    data = {"count":f"{bakingNum}","time":f"{newTime.strftime('%Y/%m/%d %H:%M:%S')}"}
    return jsonify(data)


#-------------------------
# デバッグ用
@app.route('/link')
def inde():
    return '<a href="/bakingCheck">移動</a>'

if __name__ == '__main__':
    app.debug = False
    app.run(host="0.0.0.0",port=5000)
