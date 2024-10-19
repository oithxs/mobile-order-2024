from flask import Flask, render_template, request,Blueprint,session,redirect,url_for
import os
import functools

admin_view = Blueprint('admin_view', __name__)


def login_required(func):
    import functools
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("username") is None:
            return redirect(url_for("/admin/login")) ##ここ
        else:
            return func(*args, **kwargs)
    return wrapper


@admin_view.route('/View')
@login_required
def view():
    try:
        # データ取得関数 or メソッド
        # 引数 なし
        return render_template("/admin/top.html")
    except:
        return render_template("/admin/message.html")


@admin_view.route('/delete/<int:id>')
@login_required
def delete():
    try:
        # データ削除関数 or メソッド
        # 引数 id
        return redirect(url_for("view",message="delete success"))
    except:
        return redirect(url_for("view",message="delete failed"))


@admin_view.route('/edit/<int:id>')
@login_required
def edit():
    try:
        # データ編集関数 or メソッド
        # 引数 id
        return redirect(url_for("view",message="edit success"))
    except:
        return redirect(url_for("view",message="edit failed"))


@admin_view.route('/system/message')
@login_required
def message():
    return render_template("/admin/message.html")


@admin_view.route('/login',methods=['GET','POST'])
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
