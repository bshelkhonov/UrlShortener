from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    flash
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required
from app.database import db

from .models import User

users_module = Blueprint("users_module", __name__)


@users_module.route("/login", methods=["GET", "POST"])
def login_page():
    login = request.form.get("login")
    password = request.form.get("password")

    if login and password:
        user = User.query.filter_by(username=login).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page)
        else:
            flash("Неверный логин или пароль")
    else:
        flash("Введите логин или пароль")

    return render_template("users_module/login.html")


@users_module.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("short_link_module.index"))


@users_module.route("/register", methods=["GET", "POST"])
def register():
    login = request.form.get("login")
    password = request.form.get("password")

    if request.method == "POST":
        print(login, password)
        if not (login and password):
            flash("Заполните все поля")
        else:
            print("register")
            password_hash = generate_password_hash(password)
            new_user = User(username=login, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("short_link_module.index"))
    return render_template("users_module/register.html")


@users_module.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(
            url_for("users_module.login_page") + "?next=" + request.url)
    return response
