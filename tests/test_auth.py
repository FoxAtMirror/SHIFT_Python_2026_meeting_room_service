from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register():

    response = client.post(
        "/auth/register",
        json={
            "login": "test_user_1",
            "password": "12345"
        }
    )

    assert response.status_code in [200, 400]

def test_login():

    response = client.post(
        "/auth/login",
        data={
            "username": "vlad",
            "password": "12345"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data