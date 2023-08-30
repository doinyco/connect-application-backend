from app.models.user import User
import pytest
import base64
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_saved_users(client, one_user):
    # Simulate a logged-in user
    with client:
        response_login = client.post(
            "/users/login",
            data={
                "username": "doinyco",
                "password": "doinacolun94"
            }
        )
    # Act 
    response = client.get("/users")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    print(response_body)
    assert response_body == [
        {
            "user_id": 1,
            "username": "doinyco",
            "email": "doinyco@gmail.com"
        }
    ]

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_user(client, one_user):
    # Simulate a logged-in user
    with client:
        response_login = client.post(
            "/users/login",
            data={
                "username": "doinyco",
                "password": "doinacolun94"
            }
        )
        assert response_login.status_code == 200

        response = client.get("/users/doinyco")
        response_body = response.get_json()

        # Assert
        assert response.status_code == 200
        assert "user" in response_body
        assert response_body["user"] == {
            "user_id": 1,
            "username": "doinyco",
            "email": "doinyco@gmail.com",
            "password": "$2b$12$DWKNJcHxWKENgvAPi4n8Bu2pQ6XI9JTd/r6bvpLLRjEmzn1yLcWXe"
        }

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_events_from_one_user(client, one_event_belongs_to_one_user):
    with client:
        response_login = client.post(
            "/users/login",
            data={
                "username": "doinyco",
                "password": "doinacolun94"
            }
        )

    file_data = base64.b64encode(b"SOME_BYTES").decode('utf-8')
    # Act 
    response = client.get("/users/1/events")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "events" in response_body
    assert len(response_body["events"]) == 1

    expected_response = {
        "user_id": 1,
        "username": "doinyco",
        "events": [
            {
            "event_id": 1,
            "title": "GWC Hiring Summit",
            "event_type": "Hiring Event",
            "location": "Virtual",
            "date": "September 8th 2023",
            "description": "Join us for this Hiring Online Event.",
            "file_data": file_data
            }
        ]
    }
    assert response_body == expected_response

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_register_one_user(client):
    # Act
    response = client.post("/users/register", json={
        "username": "doinyco",
        "email": "doinyco@gmail.com",
        "password": "testpassword1"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "message": "Registration successful"
    }
    
    new_user = User.query.get(1)
    assert new_user
    assert new_user.username == "doinyco"
    assert new_user.email == "doinyco@gmail.com"
    assert bcrypt.check_password_hash(new_user.password, "testpassword1")

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_update_user(client, one_user):
    with client:
        response_login = client.post(
            "/users/login",
            data = {
                "username": "doinyco",
                "password": "doinacolun94"
            }
        )
    new_password = bcrypt.generate_password_hash("testpassword2023").decode('utf-8')

    response = client.put("/users/1", json={
        "username": "doinyco",
        "email": "doinaco@gmail",
        "password": new_password
    })
   
    # Assert
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "User with ID 1 successfully updated."
    
# @pytest.mark.skip(reason="No way to test this feature yet")
def test_logout_user(client, one_user):
    with client:
        response_login = client.post(
            "/users/login",
            data={
                "username": "doinyco",
                "password": "doinacolun94"
            }
        )
        assert response_login.status_code == 200

        response_logout = client.post("/users/logout")
        assert response_logout.status_code == 200

        response_body = response_logout.get_json()
        assert "message" in response_body
        assert response_body["message"] == "Logged out successfully"

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_user(client, one_user):
    with client:
        response_login = client.post(
            "/users/login",
            data={
                "username": "doinyco",
                "password": "doinacolun94"
            }
        )
    # Act
    response = client.delete("/users/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "message" in response_body
    assert response_body == {
        "message": "User with ID 1 successfully deleted."
    }
    
    # assert User.query.get(1) == None