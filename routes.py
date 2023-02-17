from flask import render_template, request
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
        return request.form

    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if request.method == "POST":
        return request.form

    return render_template("signup.html", form=form)