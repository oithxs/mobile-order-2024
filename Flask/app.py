#-------------------------------------------------------------------------------
## 変更なし
from flask import Flask, render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import sys
import datetime

app = Flask(__name__)

# envファイルを読み込む
load_dotenv()
user = os.environ['USER']
password = os.environ['PASSWORD']
db = os.environ['DB']
host = os.environ['HOST']

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
    number = db.Column(db.Integer)
    

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
    import datetime
    return datetime.datetime.now()

# バックアップデータの書き込み
def backUpWrite(count :int):
    backUp = open('backUpNum.txt','w')
    backUp.write(str(count))
    backUp.close()

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
from datetime import timedelta
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
import datetime
@app.route('/bakingCheck')
def BakingCheck():
    # 焼かなければならない数を取得
    return render_template("admin/bakingCheck.html")

# 焼かなければならない数をリセットするページ
@app.route('/bakingCountReset')
def bakingCountReset():
    global bakingNum
    global newTime
    bakingNum = 0
    newTime = nowTime()
    backUpWrite(bakingNum)
    return "<p>処理中です...</p><script>window.location.href = 'bakingCheck';</script>"

# 情報を取得(JSON形式で返却)
@app.route('/getData')
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