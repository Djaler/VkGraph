from flask import jsonify, request

from .. import app
from ..model.response import Response, Status
from ..services import friends_chain, mutual_friends, vk


@app.route("/api/user")
def get_user():
    user_id = request.args.get("userId")
    
    try:
        user = vk.get_user(user_id)
        if vk.get_friends_count(user.id) > 0:
            response = Response(Status.OK, dict(id=user.id,
                                                name=user.name,
                                                photo=user.photo,
                                                link=user.link))
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

    friends, mutual_ids = mutual_friends.get_mutual_friends(user_id)

    friends = [dict(id=user.id,
                    name=user.name,
                    photo=user.photo,
                    color=user.color) for user in friends]

    connections = []
    for friend_id, mutual_friends_ids in mutual_ids.items():
        for mutual_friend_id in mutual_friends_ids:
            if dict(target=mutual_friend_id,
                    source=friend_id) not in connections:
                connections.append(dict(source=mutual_friend_id,
                                        target=friend_id))

    response = Response(Status.OK, dict(friends=friends,
                                        friends_connections=connections))
    
    return jsonify(response)


@app.route("/api/friends_chain")
def get_friends_chain():
    user1_id = int(request.args.get("user1Id"))
    user2_id = int(request.args.get("user2Id"))
    chain_length = int(request.args.get("chainLength"))
    
    chain = friends_chain.get_chain(user1_id, user2_id, chain_length)
    
    if chain is not None:
        users = [dict(name=user.name,
                      photo=user.photo,
                      link=user.link) for user in vk.get_users(chain)]
        response = Response(Status.OK, users)
    else:
        response = Response(Status.OK, None)
    
    return jsonify(response)
