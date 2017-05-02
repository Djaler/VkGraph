from flask import Response, jsonify, render_template, request

from . import app, vk


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

    friends = {user.id: user for user in vk.get_friends(user.id)}
    friends[user.id] = user

    mutual_friends = vk.get_mutual_friends(list(friends.keys()), user.id)

    nodes = [dict(id=id, label=friend.name, image=friend.photo) for id, friend
             in friends.items()]

    edges = []
    for friend_id, links in mutual_friends.items():
        for link in links:
            if {"target": link, "source": friend_id} not in edges:
                edge = {"target": friend_id, "source": link}
                edges.append(edge)

    return jsonify(dict(nodes=nodes, edges=edges))
