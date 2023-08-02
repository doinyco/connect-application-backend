from flask import Blueprint, abort, make_response, jsonify, request
from app import db
from app.models.user import User
from app.models.event import Event


users_bp = Blueprint("user_bp", __name__, url_prefix="/user")
events_bp = Blueprint("events_bp", __name__, url_prefix="/events")

def validate_user_id(user_id):
    try:
        user_id = int(user_id)
    except:
        return abort(make_response(jsonify({"message": f"Invalid user with ID {user_id} "}), 400))

    user = User.query.get(user_id)

    if user is None:
        return abort(make_response(jsonify({"message": f"User with id {user_id} not found."}), 404))
    
    return user

def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()

    return user

# CREATE NEW USER
@users_bp.route("", methods=["POST"])
def create_user():
    request_body = request.get_json()
    
    new_user = User(
        # user_id=request_body["user_id"],
        username=request_body["username"],
        email=request_body["email"]
    )
    db.session.add(new_user)
    db.session.commit()

    return {
        "username": new_user.username,
        "message": f"Successfully created username {new_user.username}"
    }, 201

# READ (GET) ONE USER 
@users_bp.route("/<username>", methods=["GET"])
def read_user(username):
    user = get_user_by_username(username)

    if user is None:
        return {
            "message": f"User {username} not found"
        }, 404

    response = {
        "user_id": user.user_id,
        "username": user.username
    }

    return jsonify({"user": response}), 200

# READ (GET) ALL USERS
@users_bp.route("", methods=["GET"])
def get_all_users():
    users = User.query.all()
    users_response = []

    for user in users:
        users_response.append({
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email
        })

    return jsonify(users_response), 200

# UPDATE USER 
@users_bp.route("/<user_id>", methods=["PUT"])
def update_user(user_id):
    user = validate_user_id(user_id)

    request_body = request.get_json()

    user.username = request_body["username"]
    user.email = request_body["email"]

    db.session.commit()

    return make_response(f"User with ID {user.user_id} successfully updated")

# # Delete user at user ID 
@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = validate_user_id(user_id)
    db.session.delete(user)
    db.session.commit()

    return {
        "message": f"User with ID {user.user_id} successfully deleted."
    }, 200








