from flask import jsonify, request

from .. import app
from ..model import User
from ..model.response import Response, Status
from ..services import vk
from ..services.friends_chain import get_friends_chain
from ..services.preparation import (prepare_friends_connections, prepare_user,
                                    prepare_users)


@app.route("/api/user")
def get_user():
    user_id = request.args.get("user_id")
    
    try:
        user = vk.get_user(user_id)
        if vk.get_friends_count(user.id) > 0:
            response = Response(Status.OK, prepare_user(user))
        else:
            response = Response(Status.ERROR, "NO_FRIENDS")
    except vk.NoUserException:
        response = Response(Status.ERROR, "NO_USER")
    except vk.UserDeactivatedException:
        response = Response(Status.ERROR, "USER_DEACTIVATED")

    return jsonify(response)


@app.route("/api/mutual_friends", methods=['POST'])
def get_mutual_friends():
    user = User.from_json(request.get_json())

    friends = vk.get_friends(user.id)
    
    mutual_friends = vk.get_mutual_friends_ids(friends, user.id)

    response = Response(Status.OK,
                        dict(friends=prepare_users(friends),
                             friends_connections=prepare_friends_connections(
                                 mutual_friends)))
    
    return jsonify(response)


@app.route("/api/friends_chain", methods=['POST'])
def get_friends_chain():
    json = request.get_json()
    user1, user2 = User.from_json(json[0]), User.from_json(json[1])
    
    chain = get_friends_chain(user1, user2, 5)
    
    if chain:
        response = Response(Status.OK, list(map(vk.get_user, chain)))
    else:
        response = Response(Status.OK, None)
    
    return jsonify(response)
