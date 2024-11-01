# 焼き時間予想システム
## 注意事項
焼き時間予想システムへは，localhost:5000にアクセスしたときに現れるリンクからアクセス
（当日は管理画面のボタン）
デバッグモードをオンにしていると正常に動作しません．オフにしてください．

requirementsに分ける前にbranchを切っていたので，Dockerfileに書いていますが，requirementsで大丈夫です．
`pip install SQLAlchemy`
`pip install cryptography`
↑暗号化用のライブラリです．ないとエラーが出ます．

焼かなければならないフランクフルトがある場合には，音が出るように実装していますが，直で，/bakingCheckにアクセスすると正しく動作しない（音が出ない）のでご注意ください．

# envファイル
BAKINGTIME=5

# backUpNum.txt
入っている数字が，初期状態の焼かなければならない数になります．

------------------------------------
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
{id, 名前，本数，ケチャップ，マスタード，予約時刻}={id, name, number, ketchup, mustard, reservationTime}
# sample.sql
試験用のサンプルデータです．
mogi.sqlを読み込んでから使用してください．