from flask import Blueprint, jsonify, request

from app.model import Chain, Response, Status, UsersGraph
from app.services import friends_chain, mutual_friends, temperature_map, vk

api = Blueprint('api', __name__)


@api.route("/api/user")
def get_user():
    user_id = request.args.get("userId")
    
    try:
        user = vk.get_user(user_id)
        if vk.get_friends_count(user.id) > 0:
            response = Response(Status.OK, user.to_json())
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


@api.route("/api/mutual_friends")
def get_mutual_friends():
    user_id = int(request.args.get("userId"))

    friends, mutual_ids = mutual_friends.get_mutual_friends(user_id)

    graph = UsersGraph(friends, mutual_ids)

    connections_counts = [len([connection for connection in graph.connections
                               if user.id in connection])
                          for user in friends]

    interval_start, interval_end = min(connections_counts), max(
        connections_counts)
    interval_length = interval_end - interval_start
    
    for user, connections_count in zip(graph.users, connections_counts):
        user.color = temperature_map.calculate_color(
            connections_count - interval_start, interval_length)
    
    response = Response(Status.OK, graph.to_json())
    
    return jsonify(response)


@api.route("/api/friends_chain")
def get_friends_chain():
    user1_id = int(request.args.get("user1Id"))
    user2_id = int(request.args.get("user2Id"))
    chain_length = int(request.args.get("chainLength"))

    chain = friends_chain.find_chain(user1_id, user2_id, chain_length)
    
    if chain is not None:
        response = Response(Status.OK, Chain(vk.get_users(chain)).to_json())
    else:
        response = Response(Status.OK, None)
    
    return jsonify(response)
