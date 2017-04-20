from flask import render_template, request, Response

from . import app
from . import vk


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/api")
def api():
    user_id = request.args.get("user_id")
    
    try:
        user_id = int(user_id)
    except ValueError:
        try:
            user_id = vk.get_id(user_id)
        except vk.NoUserException:
            return Response(status=400)
    
    friends = {user.id: user for user in vk.get_friends(user_id)}
    
    mutual_friends = vk.get_mutual_friends(list(friends.keys()), user_id)
    
    return str(mutual_friends)
