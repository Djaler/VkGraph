from flask import redirect, render_template, url_for

from . import app


@app.route("/")
@app.route("/index")
def index_page():
    return redirect(url_for("mutual_friends_page"))


@app.route("/mutual_friends")
def mutual_friends_page():
    return render_template("mutual_friends.html")


@app.route("/deep_search")
def deep_search_page():
    return redirect(url_for("index_page"))
