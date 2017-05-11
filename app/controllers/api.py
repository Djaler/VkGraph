from flask import jsonify, request

from .. import app
from ..model.response import Response, Status
from ..services import friends_chain, vk
from ..services.preparation import (prepare_friends_connections, prepare_user,
                                    prepare_users)


@app.route("/api/user")
def get_user():
    user_id = request.args.get("userId")
    
    try:
        user = vk.get_user(user_id)
        if vk.get_friends_count(user.id) > 0:
            response = Response(Status.OK, prepare_user(user))
        else:
            response = Response(Status.ERROR,
                                "У пользователя с id {} отсутствуют или "
                                "скрыты друзья".format(user_id))
    except vk.NoUserException:
        response = Response(Status.ERROR, "Пользователя с id {} не "
                                          "существует".format(user_id))
    except vk.UserDeactivatedException:
        response = Response(Status.ERROR,
                            "Пользователь с id {} деактивирован".format(
                                user_id))
    
    return jsonify(response)


@app.route("/api/mutual_friends")
def get_mutual_friends():
    user_id = int(request.args.get("userId"))
    
    friends = vk.get_friends(user_id)
    
    mutual_friends = vk.get_mutual_friends_ids(friends, user_id)
    
    response = Response(Status.OK,
                        dict(friends=prepare_users(friends),
                             friends_connections=prepare_friends_connections(
                                 mutual_friends)))
    
    return jsonify(response)


@app.route("/api/friends_chain")
def get_friends_chain():
    user1_id = int(request.args.get("user1Id"))
    user2_id = int(request.args.get("user2Id"))
    chain_length = int(request.args.get("chainLength"))
    
    chain = friends_chain.get_chain(user1_id, user2_id, chain_length)
    
    if chain is not None:
        response = Response(Status.OK,
                            [prepare_user(vk.get_user(user)) for user in
                             chain])
    else:
        response = Response(Status.OK, None)
    
    return jsonify(response)
