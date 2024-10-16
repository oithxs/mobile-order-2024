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
def admin():
    return render_template("/admin/top.html")

@admin_view.route('/delete')
@login_required
def delete():
    return redirect("/view")

@admin_view.route('/edit')
@login_required
def edit():
    return redirect("/view")


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
