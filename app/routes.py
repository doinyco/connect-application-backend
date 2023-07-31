from flask import Blueprint, abort, make_response, jsonify, request

class User:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email

users_bp = Blueprint("user_bp", __name__, url_prefix="/users")

users = {
    1: User(1, "doinac", "doinyco@gmail.com"),
    2: User(2, "gabbycl", "gabbcl@gmail.com"),
    3: User(3, "fernafd", "ferdd@gmail.com"),
    4: User(4, "bruce", "bras@gmail.com"),
    5: User(5, "panda", "pandax1@gmail.com")
}

def validate_user_id(user_id):
    try:
        user_id = int(user_id)
    except:
        return abort(make_response(jsonify({"message": f"Invalid user with ID {user_id} "}), 400))

    if user_id not in users:
        abort(make_response({"message": f"User with id {user_id} not found."}, 404))
    else:
        return users[user_id]


# CREATE NEW USER
@users_bp.route("", methods=["POST"])
def create_user():
    request_body = request.get_json()
    new_user = User(
        user_id=request_body["user_id"],
        username=request_body["username"],
        email=request_body["email"]
    )

    users[new_user.user_id] = new_user

    return make_response(f"User with id {new_user.user_id} successfully created!", 201)

# READ (GET) ONE USER 
@users_bp.route("/<user_id>", methods=["GET"])
def read_user(user_id):
    user = validate_user_id(user_id)

    return jsonify({
        "user_id":user.user_id,
        "username":user.username,
        "email":user.email
    })

# READ (GET) ALL USERS
@users_bp.route("", methods=["GET"])
def get_all_users():
    users_response = []

    for user in users:
        user = users[user]
        users_response.append({
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email
        })

    return jsonify(users_response), 200

# Delete user at user ID 
@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = validate_user_id(user_id)
    users.pop(int(user_id))

    return make_response(f"User with id {user.user_id} successfully deleted.", 200)






    