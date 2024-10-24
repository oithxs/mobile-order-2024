
from flask import Flask, render_template, request,request,session,redirect,url_for
from admin_view import admin_view
from flask_sqlalchemy import SQLAlchemy
import functools
import os
from dotenv import load_dotenv

# envファイルを読み込む
load_dotenv()
user = os.environ['USER']
password = os.environ['PASSWORD']
db = os.environ['DB']
host = os.environ['HOST']


app = Flask(__name__)

app.register_blueprint(admin_view,url_prefix="/admin")
app.secret_key = os.urandom(24)

db_uri = f'mysql+pymysql://{user}:{password}@{host}/{db}?charset=utf8'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
# ---------------------------------------------------------------------------
# DB生成処理
class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.Text())
    number = db.Column(db.Integer)
    ketchup = db.Column(db.Boolean)
    mustard = db.Column(db.Boolean)
    reservationTime = db.Column(db.DateTime)

class Nickname(db.Model):
    __tablename__ = 'nickname'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.Text())
    status = db.Column(db.Boolean)

class Received(db.Model):
    __tablename__ = 'received'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.Text())
    number = db.Column(db.Boolean)
# ---------------------------------------------------------------------------
# adminの削除処理
def destroy(id):
    message = "Destroy SQLAlchemy"

    # データ削除
    reservation = Reservation.query.get(id)
    db.session.delete(reservation)
    db.session.commit()

    return 'ok'
# ---------------------------------------------------------------------------
# /adminと/userの取得処理
from datetime import datetime

#user side
def get_nicknames():
    nicknames = Nickname.query.all()
    return nicknames

# user side True
# admin side False
"""ここわからん"""
def update_nickname_status1(session,id: int, new_status: bool):
    nickname_record = session.query.get(id)
    if nickname_record:
        nickname_record.status = new_status
        db.session.commit()
    else:
        print("Nickname not found")

"""ここはデータベースに何を追加するプログラム"""
def add_reservation(name: str, number: int, ketchup: bool, mustard: bool, now_time: datetime):
    new_reservation = Reservation(
        name=name,
        number=number,
        ketchup=ketchup,
        mustard=mustard,
        reservationTime=now_time
    )
    db.session.add(new_reservation)
    db.session.commit()

"""
これはどこから呼び出されることを想定した？
履歴画面？それともadminの一覧画面？
どちらにしろ、履歴画面と一覧画面で二種類必要だと思う
"""
def get_reservations():
    reservations = Reservation.query.all()
    return reservations
# ---------------------------------------------------------------------------
# /adminの編集処理

def update_reservation_by_id(id: int, name: str, number: int, ketchup: bool, mustard: bool, now_time: datetime):
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
        print(f"{dt.id} {dt.name} {dt.number} {dt.ketchup} {dt.mustard} {dt.reservationTime}")


"""
#################################################ルーティング部#################################################
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
"""

@app.route('/')
def top():

    show_nickname(get_nicknames())

    update_nickname_status(Nickname,2,True)

    add_reservation("枚方太郎",10,True,False,datetime.now())

    show_reservation(get_reservations())

    update_reservation_by_id(1,"紺扉宇太",120,False,False,datetime.now())

    return 'ok'


@app.route('/View')
@login_required
def view():
    try:
        reservations=get_reservations()
        return render_template("/admin/top.html",reservations=reservations)
    except:
        return render_template("/admin/message.html",message="view failed")


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    try:
        # データ削除関数 or メソッド
        # 引数 id
        destroy(id)
        # これはたぶんいるけど T F のどちらにするべき
        # update_nickname_status1(id=id,new_status=False)
        return redirect(url_for("view",message="delete success"))
    except:
        return redirect(url_for("view",message="delete failed"))


@app.route('/edit/<int:id>')
@login_required
def edit(id):
    try:
        name=None,number=None,ketchup=None,mustard=None,datetime=None
        """
        request.formによって振り分ける
        """
        # データ編集関数 or メソッド
        # 引数 id
        update_nickname_status(id,name,number,ketchup,mustard,datetime)
        return redirect(url_for("view",message="edit success"))
    except:
        return redirect(url_for("view",message="edit failed"))


@app.route('/system/message')
@login_required
def message():
    return render_template("/admin/message.html")



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == os.environ.get("USER") and password == os.environ.get("PASSWORD"):
            session["username"] = username

            return redirect("/view")


        else:
            return render_template("/admin/login.html")
    else:
        return render_template("/admin/login.html")




def login_required(func):
    import functools
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("username") is None:

            return redirect(url_for("/admin/login")) ##ここ

        else:
            return func(*args, **kwargs)
    return wrapper




if __name__ == '__main__':
    app.debug = True
    app.run()
