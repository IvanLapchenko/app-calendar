from flask import render_template
from .forms import LoginForm, SignupForm
from . import app

@app.route("/")
@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/signup")
def signup():
    form = SignupForm()
    return render_template("signup.html", form=form)