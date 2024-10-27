# テスト用のシステムです．本番用ではありません．
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# envファイルを読み込む
load_dotenv()
user = os.environ['USER']
password = os.environ['PASSWORD']
db = os.environ['DB']
host = os.environ['HOST']

app = Flask(__name__)

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
@app.route('/destroy/<int:id>')
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

def get_nicknames():
    nicknames = Nickname.query.all()
    return nicknames

def update_nickname_status1(session,id: int, new_status: bool):
    nickname_record = session.query.get(id)
    if nickname_record:
        nickname_record.status = new_status
        db.session.commit()
    else:
        print("Nickname not found")

def update_nickname_status2(session,nickName: str, new_status: bool):
    nickname_record = session.query.all()
    for oneNickName in nickname_record:
        if(oneNickName.name==nickName):
            update_nickname_status1(session,oneNickName.id,new_status)
            return  True
    print("Nickname not found")
    return  False


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

def get_reservations():
    reservations = Reservation.query.all()
    return reservations

def getOrderHistory(id: int):
    order = Reservation.query.get(id)
    name = order.name
    number = order.number
    ketchup = order.ketchup
    mustard = order.mustard
    reservationTime = order.reservationTime
    return name,number,ketchup,mustard,reservationTime

# ---------------------------------------------------------------------------
# /adminの編集処理
def update_reservation_by_id(id: int, name: str, number: int, ketchup: bool, mustard: bool, now_time: datetime):
    reservation = Reservation.query.get(id)
    
    if reservation:
        reservation.name = name
        reservation.number = number
        reservation.ketchup = ketchup
        reservation.mustard = mustard
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

@app.route('/')
def top():

    show_nickname(get_nicknames())

    update_nickname_status1(Nickname,2,True)

    add_reservation("枚方太郎",10,True,False,datetime.now())

    show_reservation(get_reservations())

    update_reservation_by_id(1,"紺扉宇太",500,False,False,datetime.now())

    print("KabayakiTarou")
    print(update_nickname_status2(Nickname,"KabayakiTarou",True))

    #存在しないときのテスト
    print("Tarou")
    print(update_nickname_status2(Nickname,"Tarou",False))

    # 履歴を取得
    name,number,ketchup,mustard,reservationTime = getOrderHistory(3)
    print(f"名前:{name} 個数:{number} ケチャップ:{ketchup} マスタード:{mustard} 予約時刻:{reservationTime}")

    return render_template("user/top.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
