from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_rooms():

    response = client.get("/rooms")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

def test_create_room():

    response = client.post(
        "/rooms",
        json={
            "name": "Conference Room Test"
        }
    )

    assert response.status_code == 200