from flask import Blueprint, abort, make_response, jsonify, request
from app import db
from app.models.event import Event
import base64
from sqlalchemy.exc import SQLAlchemyError

events_bp = Blueprint("events_bp", __name__, url_prefix="/events")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# POST (CREATE) EVENT
@events_bp.route("/create_event", methods=["POST"])
def create_event():
    try:
        title = request.form.get("title")
        event_type = request.form.get("event_type")
        location = request.form.get("location")
        date = request.form.get("date")
        description = request.form.get("description")
        user_id = int(request.form.get("user_id"))

        if "file" in request.files:
            file = request.files["file"]

            if file.filename == "":
                return jsonify(message="Please upload a photo"), 400

            if file and allowed_file(file.filename):
                file_data = file.read()

                new_event = Event(
                    title=title,
                    event_type=event_type,
                    location=location,
                    date=date,
                    description=description,
                    user_id=user_id,
                    file_data=file_data
                )

                db.session.add(new_event)
                db.session.commit()

                return jsonify(message="Event created successfully"), 201

            return jsonify(message="Invalid file format"), 400

        return jsonify(message="File is missing"), 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(message="An error occurred while saving the event"), 500

    except Exception as e:
        return jsonify(message="An error occurred"), 500

# READ (GET) ONE EVENT 
@events_bp.route("/<event_id>", methods=["GET"])
def read_event(event_id):
    event = get_event_or_abort(event_id)

    response = {
            "event_id": event.event_id,
            "title": event.title,
            "event_type": event.event_type,
            "location": event.location,
            "date": event.date,
            "description": event.description,
            "user_id": event.user_id,
            "file_data": base64.b64encode(event.file_data).decode('utf-8') if event.file_data else None
        }
    return jsonify({"event": response}), 200

# READ (GET) ALL EVENTS
@events_bp.route("", methods=["GET"])
def get_events():
    events = Event.query.all()
    event_list = []

    for event in events:
        event_data = {
            "event_id": event.event_id,
            "title": event.title,
            "event_type": event.event_type,
            "location": event.location,
            "date": event.date,
            "description": event.description,
            "user_id": event.user_id,
            "file_data": base64.b64encode(event.file_data).decode('utf-8') if event.file_data else None
        }
        event_list.append(event_data)

    return jsonify(event_list)
        
# PUT (UPDATE) EVENT
@events_bp.route("/<event_id>", methods=["PUT"])
def update_event(event_id):
    event = get_event_or_abort(event_id)
    request_body = request.form

    event.title = request_body["title"]
    event.event_type = request_body["event_type"]
    event.location = request_body["location"]
    event.date = request_body["date"]
    event.description = request_body["description"]

    if "file" in request.files:
        file = request.files["file"]

        if file.filename == "":
            return jsonify(message="No selected file"), 400
        
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