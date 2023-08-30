import pytest
from app import create_app
from flask.signals import request_finished
from app import db
from app.models.user import User
from app.models.event import Event
import logging

@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()

def test_print_database_uri(caplog):
    # Get the app with the test configuration
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "SQLALCHEMY_TEST_DATABASE_URI"})

    # Access the app context to trigger the database URI print
    with app.app_context():
        # Use caplog to capture log output
        with caplog.at_level(logging.DEBUG):
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            print(f"Database URI: {db_uri}")
        
        # Your test assertions here
        assert db_uri == "SQLALCHEMY_TEST_DATABASE_URI"

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_event(app):
    file_data = b"SOME_BYTES"
    user = User.query.first()

    new_event = Event(
        title = "GWC Hiring Summit",
        event_type = "Hiring Event",
        location = "Virtual",
        date = "September 8th 2023",
        description = "Join us for this Hiring Online Event.",
        file_data = file_data,
        user = user
    )
    db.session.add(new_event)
    db.session.commit()

@pytest.fixture
def two_events(app):
    file_data1 = b"SOME_BYTES_1"
    file_data2 = b"SOME_BYTES_2"
    db.session.add_all([
        Event(
            title="NAICA Hiring Event",
            event_type="Hiring Event",
            location="215 East 99th Street Manhattan, NY 10029",
            date="August 29 2023",
            description="Bring your resume and a smile! On TUESDAY August 29th, 2023 (4:00 p.m.-7:00 p.m.) located at 2﻿15 East 99th Street New York, New York 10029.",
            file_data=file_data1, 
            user_id = 1
        ),
        Event(
            title="Hiring event at Curtis Caldwell Center",
            event_type="Hiring Event",
            location="4999 Naaman Forest Boulevard Garland, TX 75040",
            date="Friday, September 8 · 7 - 10pm CDT",
            description="None",
            file_data=file_data2, 
            user_id = 1
        )
    ])
    db.session.commit()

@pytest.fixture
def one_user(app):
    new_user = User(
        username="doinyco", 
        email="doinyco@gmail.com", 
        password="$2b$12$DWKNJcHxWKENgvAPi4n8Bu2pQ6XI9JTd/r6bvpLLRjEmzn1yLcWXe"
    )
    db.session.add(new_user)
    db.session.commit()

@pytest.fixture
def one_event_belongs_to_one_user(app, one_event, one_user):
    user = User.query.first()
    event = Event.query.first()
    event.user = user
    db.session.commit()