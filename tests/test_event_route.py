from app.models.event import Event
import pytest
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_event_no_saved_events(client):
    # Act 
    response = client.get("/events")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_event(client, one_event):
    # Act 
    response = client.get("/events/1")
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 200
    assert "event" in response_body
    assert response_body == {
        "event": {
            "event_id": 1,
            "title": "GWC Hiring Summit", 
            "event_type": "Hiring Event",
            "location": "Virtual", 
            "date": "September 8th 2023", 
            "description": "Join us for this Hiring Online Event.", 
            "user_id": None,
            "file_data": "U09NRV9CWVRFUw=="
    }}

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_saved_events(client, one_event):
    # Act 
    response = client.get("/events")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "event_id": 1,
            "title": "GWC Hiring Summit",
            "event_type": "Hiring Event",
            "location": "Virtual",
            "date": "September 8th 2023",
            "description": "Join us for this Hiring Online Event.",
            "user_id": None,
            "file_data": "U09NRV9CWVRFUw==",
        }
    ]

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_update_event(client, one_event):
    form_data = {
        "title":"GWC Hiring Summit",
        "event_type":"Hiring Event",
        "location":"450 110th Ave NE, Bellevue, WA 98004",
        "date": "September 15th 2023",
        "description": "Join us for this Hiring Online Event.",
        "user_id": 1 ,
        "file_data": "U09NRV9CWVRFUw=="
    }
    response = client.put("/events/1", data=form_data)
    assert response.status_code == 200

    response_data = response.get_data(as_text=True)
    expected_message = f"Event with ID 1 successfully updated"
    assert expected_message in response_data

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_event(client, one_event):
    # Act
    response = client.delete("/events/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "message" in response_body
    assert response_body == {
        "message": "Event with ID 1 successfully deleted."
    }
    assert Event.query.get(1) == None

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_event_not_found(client):
    # Act
    response = client.delete("/events/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": f"Event with ID 1 not found."}
    assert Event.query.all() == []

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_non_existent_event(client):
    # Act
    response = client.get("/events/100")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Event with ID 100 not found."}