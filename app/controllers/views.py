from flask import redirect, render_template, url_for

from .. import app, cache


def never():
    return False


@app.route("/")
@app.route("/index")
@cache.cached(unless=never)
def index_page():
    return redirect(url_for("mutual_friends_page"))


@app.route("/mutual_friends")
@cache.cached(unless=never)
def mutual_friends_page():
    return render_template("mutual_friends.html")


@app.route("/friends_chain")
@cache.cached(unless=never)
def friends_chain_page():
    return render_template("friends_chain.html")
