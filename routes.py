from flask import render_template, request, redirect, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .communicate_with_db import add_item_to_db, get_user_by_nickname
from .database import User
from .forms import LoginForm, SignupForm
from . import app


@app.route("/")
@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        user = get_user_by_nickname(form.nickname.data)

        if user:
            is_password_correct = check_password_hash(user.password, form.password.data)

            if is_password_correct:
                login_user(user)
                return redirect("main")

            flash("Password is incorrect. ")

        flash("There is no user with this name. ")
        return redirect("login")
    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if request.method == "POST":

        user = get_user_by_nickname(form.nickname.data)

        if user:
            flash("This user already exists. ")
            return redirect("signup")

        password = generate_password_hash(form.password.data)
        user = User(nickname=form.nickname.data, email=form.email.data, password=password)
        add_item_to_db(user)

        return redirect("login")

    return render_template("signup.html", form=form)