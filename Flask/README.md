# 必要なライブラリ
* PyMySQL
* Flask-SQLAlchemy
* python-dotenv
# envファイル
* USER='ユーザー名'
* PASSWORD='パスワード'
* DB='データベース名'
* HOST='ホスト'
# mogi.sql
## テーブル
`source mogi;`で読み込む
### nickname
ニックネームのテーブル<br>
クラス名：Nickname<br>
{id, ニックネーム, 空き状況}={id, name, status}
### received
受け取り済みのテーブル<br>
クラス名：Received<br>
{id, 名前, 本数}={id, name, number}
### reservation
注文用テーブル<br>
クラス名：Order<br>
{id, 名前，本数，ケチャップ，マスタード，予約時刻｝={id, name, number, ketchup, mustard, time}
# sample.sql
試験用のサンプルデータです．
mogi.sqlを読み込んでから使用してください．