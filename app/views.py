from flask import Response, jsonify, render_template, request

from . import app, vk
from .preparation import prepare_edges, prepare_nodes


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/mutual_friends")
def get_mutual_friends():
    user_id = request.args.get("user_id")
    
    try:
        user = vk.get_user(user_id)
    except vk.NoUserException:
        return Response(status=400)

    friends = vk.get_friends(user.id) + [user]

    mutual_friends = vk.get_mutual_friends_ids(friends, user.id)

    return jsonify(dict(nodes=prepare_nodes(friends),
                        edges=prepare_edges(mutual_friends)))
