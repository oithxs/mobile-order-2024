from flask import Flask, render_template, request,Blueprint,session,redirect,url_for
import os
import functools

admin_view = Blueprint('admin_view', __name__)

def login_required(func):
    import functools
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("username") is None:
            return redirect(url_for("login")) ##ここ
        else:
            return func(*args, **kwargs)
    return wrapper


@admin_view.route('/view')
@login_required
def admin(msg=None):
    # データ取得メソッド or 関数
    return render_template("/admin/top.html",data=data,msg=msg)


@admin_view.route('/delete',methods=['POST'])
@login_required
def delete():
    try:
        # データ削除メソッド or 関数
        return redirect(url_for("admin_view.admin"),msg="delete success!")
    except:
        return redirect(url_for("admin_view.admin"),msg="delete error")


@admin_view.route('/edit',methods=['POST'])
@login_required
def edit():
    try:
        # データ書き込みメソッド or 関数
        return redirect(url_for("admin_view.admin"),msg="edit success!")
    except:
        return redirect(url_for("admin_view.admin"),msg="edit error")


@admin_view.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == os.environ.get("USER") and password == os.environ.get("PASSWORD"):
            session["username"] = username
            return redirect(url_for("admin_view.admin"),msg="login success!")
        else:
            return render_template("/admin/login.html")
    else:
        return render_template("/admin/login.html")
