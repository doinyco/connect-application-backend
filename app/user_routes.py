from flask import Blueprint, abort, make_response, jsonify, request
from app import db
from app.models.login import LoginForm
from app.models.register import RegisterForm
from app.models.user import User
import base64
from flask_login import LoginManager, login_user, login_required, logout_user, LoginManager
from app.models.login import LoginForm
from app.models.register import RegisterForm
from flask_bcrypt import Bcrypt
import logging

login_manager = LoginManager()
bcrypt = Bcrypt()
login_manager.login_view = "login"

users_bp = Blueprint("user_bp", __name__, url_prefix="/users")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    return User.query.filter_by(username=username).first()

# REGISTER (CREATE) ONE USER
@users_bp.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    response_data = {}

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            response_data["error"] = "Username already exists"
            return jsonify(response_data), 400

        # Create a new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        response_data["message"] = "Registration successful"
        return jsonify(response_data), 201

    response_data["errors"] = form.errors
    return jsonify(response_data), 400

# LOGIN USER
@users_bp.route("/login", methods=["POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            logging.debug(f"Form Password: {form.password.data}")
            logging.debug(f"Database Hashed Password: {user.password}")
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return make_response(jsonify(message="Logged in successfully"), 200)
    return make_response(jsonify(message="Invalid username or password"), 401)

# LOGOUT USER
@users_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify(message="Logged out successfully"), 200

# READ (GET) ONE USER 
@users_bp.route("/<username>", methods=["GET"])
@login_required
def read_user(username):
    user = get_user_by_username(username)

    if user is None:
        return {
            "message": f"User {username} not found"
        }, 404

    response = {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "password": user.password
    }
    return jsonify({"user": response}), 200

# READ (GET) ALL USERS
@users_bp.route("", methods=["GET"])
@login_required
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

# READ ALL EVENTS FROM ONE USER
@users_bp.route("/<user_id>/events", methods=["GET"])
@login_required
def read_events_from_user(user_id):
    user = validate_user_id(user_id)
    events_response = []

    for event in user.events:
        event_data = {
            "event_id": event.event_id,
            "title": event.title,
            "event_type": event.event_type,
            "location": event.location,
            "date": event.date,
            "description": event.description,
            "file_data": base64.b64encode(event.file_data).decode('utf-8') if event.file_data else None
        }
        events_response.append(event_data)

    return jsonify({
        "user_id": user.user_id,
        "username": user.username,
        "events": events_response
    }), 200

# UPDATE USER 
@users_bp.route("/<user_id>", methods=["PUT"])
@login_required
def update_user(user_id):
    user = validate_user_id(user_id)
    request_body = request.get_json()

    user.username = request_body["username"]
    user.email = request_body["email"]
    
    new_password = request_body["password"]
    if new_password:
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password

    db.session.commit()

    return make_response(f"User with ID {user.user_id} successfully updated.")

# DELETE USER
@users_bp.route("/<user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id):
    user = validate_user_id(user_id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"User with ID {user.user_id} successfully deleted."}), 200