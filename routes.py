from flask import render_template
from . import app


@app.route("/main")
def main():
    return render_template("main.html")

