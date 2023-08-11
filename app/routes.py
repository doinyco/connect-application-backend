from flask import Blueprint, abort, make_response, jsonify, request, render_template
from app import db
from app.models.user import User
from app.models.event import Event
import base64
from sqlalchemy.exc import SQLAlchemyError

users_bp = Blueprint("user_bp", __name__, url_prefix="/user")
events_bp = Blueprint("events_bp", __name__, url_prefix="/events")

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}

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

def get_event_or_abort(event_id):
    try:
        event_id = int(event_id)
    except ValueError:
        response = {"message": "Invalid data!"}
        abort(make_response(jsonify(response), 400))

    get_event = Event.query.get(event_id)
    
    if get_event is None:
        response = {"message": f"Event with ID {event_id} not found."}
        abort(make_response(jsonify(response), 404))
    
    return get_event

# CREATE NEW USER
@users_bp.route("", methods=["POST"])
def create_user():
    request_body = request.get_json()

    new_user = User(
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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@events_bp.route('/create_event', methods=['POST'])
def create_event():
    try:
        title = request.form.get('title')
        event_type = request.form.get('event_type')
        location = request.form.get('location')
        date = request.form.get('date')
        description = request.form.get('description')
        user_id = int(request.form.get('user_id'))

        if 'file' in request.files:
            file = request.files['file']

            if file.filename == '':
                return jsonify(message='Please upload a photo'), 400

            if file and allowed_file(file.filename):
                file_data = file.read()

                new_event = Event(
                    title=title,
                    event_type=event_type,
                    location=location,
                    date=date,
                    description=description,
                    user_id=user_id,
                    file_data=file_data  # Store the binary image data in the database
                )

                db.session.add(new_event)
                db.session.commit()

                return jsonify(message="Event created successfully"), 201
            else:
                return jsonify(message='Invalid file format'), 400

        else:
            return jsonify(message='File is missing'), 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(message='An error occurred while saving the event'), 500

    except Exception as e:
        return jsonify(message='An error occurred'), 500

@events_bp.route("", methods=['GET'])
def get_events():
    events = Event.query.all()
    event_list = []

    for event in events:
        event_data = {
            'event_id': event.event_id,
            'title': event.title,
            'event_type': event.event_type,
            'location': event.location,
            'date': event.date,
            'description': event.description,
            'user_id': event.user_id,
            'file_data': base64.b64encode(event.file_data).decode('utf-8') if event.file_data else None
        }
        event_list.append(event_data)

    # return jsonify(event_list)
    return render_template('index.html', events=event_list)

# READ ALL EVENTS FROM ONE USER
@users_bp.route("/<user_id>/events", methods=["GET"])
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


# READ (GET) ALL EVENTS
@events_bp.route("", methods=["GET"])
def get_all_events():
    events = Event.query.all()
    events_response = []

    for event in events:
        events_response.append({
            "event_id": event.event_id,
            "title": event.title,
            "event_type": event.event_type,
            "location": event.location,
            "date": event.date,
            "description": event.description,
            "file": event.file
        })

    return jsonify(events_response), 200
        
# UPDATE EVENT
@events_bp.route("/<event_id>", methods=["PUT"])
def update_event(event_id):
    event = get_event_or_abort(event_id)
    request_body = request.form

    event.title = request_body["title"]
    event.event_type = request_body["event_type"]
    event.location = request_body["location"]
    event.date = request_body["date"]
    event.description = request_body["description"]

    if 'file' in request.files:
        file = request.files['file']

        if file.filename == '':
            return jsonify(message='No selected file'), 400
        
        if file and allowed_file(file.filename):
            file_data = file.read()
            event.file_data = file_data

    db.session.commit()

    return make_response(f"Event with ID {event.event_id} successfully updated")

# DELETE EVENT
@events_bp.route("/<event_id>", methods=["DELETE"])
def delete_event(event_id):
    chosen_event = get_event_or_abort(event_id)

    db.session.delete(chosen_event)
    db.session.commit()

    return {
        "message": f"Event with ID {chosen_event.event_id} successfully deleted."
    }, 200