from flask import jsonify, render_template, request

from . import app, vk
from .model import User
from .preparation import prepare_edges, prepare_nodes, prepare_user
from .response import Response, Status


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/user")
def get_user():
    user_id = request.args.get("user_id")
    
    try:
        user = vk.get_user(user_id)
        response = Response(Status.OK, prepare_user(user))
    except vk.NoUserException:
        response = Response(Status.ERROR, "NO_USER")
    except vk.UserDeactivatedException:
        response = Response(Status.ERROR, "USER_DEACTIVATED")

    return jsonify(response)


@app.route("/mutual_friends", methods=["POST"])
def get_mutual_friends():
    user = User.from_json(request.get_json())
    
    friends = vk.get_friends(user.id) + [user]
    
    mutual_friends = vk.get_mutual_friends_ids(friends, user.id)
    
    response = Response(Status.OK, dict(nodes=prepare_nodes(friends),
                                        edges=prepare_edges(mutual_friends)))
    
    return jsonify(response)
