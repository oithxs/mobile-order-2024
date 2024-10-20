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

# DB生成処理
class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.Text())
    number = db.Column(db.Integer)
    ketchup = db.Column(db.Boolean)
    mustard = db.Column(db.Boolean)

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

# adminの削除処理
@app.route('/destroy/<int:id>')
def destroy(id):
    message = "Destroy SQLAlchemy"

    # データ削除
    order = Reservation.query.get(id)
    db.session.delete(order)
    db.session.commit()

    return 'ok'

if __name__ == '__main__':
    app.debug = True
    app.run()
