def test_register(client):

    response = client.post(
        "/api/auth/register",
        json={
            "login": "test_user_1",
            "password": "12345"
        }
    )

    assert response.status_code == 200

def test_login(client):

    response = client.post(
        "/api/auth/login",
        data={
            "username": "test_user_1",
            "password": "wrong_password"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid login or password"


def test_invalid_token(client):

    response = client.get(
        "/api/auth/me",
        headers={
            "Authorization": "Bearer invalid_token"
        }
    )

    assert response.status_code == 401