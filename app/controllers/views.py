from flask import Blueprint, redirect, render_template, url_for

from app import cache

views = Blueprint('views', __name__)


def never():
    return False


@views.route("/")
@views.route("/index")
@cache.cached(unless=never)
def index_page():
    return redirect(url_for(".mutual_friends_page"))


@views.route("/mutual_friends")
@cache.cached(unless=never)
def mutual_friends_page():
    return render_template("mutual_friends.html")


@views.route("/friends_chain")
@cache.cached(unless=never)
def friends_chain_page():
    return render_template("friends_chain.html")
