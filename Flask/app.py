## 焼き時間予測システム
## debugモードはオフにしてください．
from flask import Flask, render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import sys
import datetime

# 正しいディレクトリで動かすこと（再生ボタン厳禁）
#---------------------------------------------------------
## 機能02
# 現在の時刻を取得する
def nowTime():
    import datetime
    return datetime.datetime.now()


#---------------------------------------------------------
## 機能00
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
#-----------------------------------------------------


# envファイルを読み込む
load_dotenv()
user = os.environ['USER']
password = os.environ['PASSWORD']
db = os.environ['DB']
host = os.environ['HOST']

#---------------------------------------------------------
## 機能01
# 焼き時間を環境変数から読み取る
# envファイルを読み込む
bakingTime = int(os.environ['BAKINGTIME']) # 焼き時間は分
#---------------------------------------------------------
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
    number = db.Column(db.Integer)



#---------------------------------------------------------
## 機能01
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



#---------------------------------------------------------
# 機能02



#---------------------------------------------------------
# 機能03
# 現在の時刻に焼き始めなければならないフランクフルトの数を取得する関数
from datetime import timedelta
from sqlalchemy import func
def get_frankfurts_to_start_baking():
    current_time = nowTime()
    bake_start_time = current_time + timedelta(minutes=bakingTime)

    cuTime = bake_start_time.strftime('%H:%M')

    # 焼き始める必要がある予約の数を取得
    frankfurts_to_start = db.session.query(func.sum(Reservation.number)).filter(func.date_format(Reservation.reservationTime, '%H:%i') == cuTime).scalar()
    if(frankfurts_to_start==None):
        return 0
    #frankfurts_to_start = db.session.query(Reservation).filter(func.date_format(Reservation.reservationTime, '%H:%i') == cuTime).all()
    
    return frankfurts_to_start


#---------------------------------------------------------
# 機能04
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



#-------------------------
# デバッグ用
@app.route('/')
def inde():
    #print(f"存在しないデータ:{reservationlate(100)}")
    #print(f"予約時刻を過ぎている:{reservationlate(1)}")
    #print(f"予約時刻を過ぎていない:{reservationlate(12)}")
    #print(f"焼き始めなければ:{get_frankfurts_to_start_baking()}")
    #テスト用
    global bakingNum
    bakingNum = 110
    return '<a href="/bakingCheck">移動</a>'

if __name__ == '__main__':
    app.debug = False
    app.run(host="0.0.0.0",port=5000)