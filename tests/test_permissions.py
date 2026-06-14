def test_me_requires_auth(client):

    response = client.get(
        "/api/auth/me"
    )

    assert response.status_code == 401


def test_my_bookings_requires_auth(client):

    response = client.get(
        "/api/bookings/my"
    )

    assert response.status_code == 401


def test_create_booking_requires_auth(client):

    response = client.post(
        "/api/bookings",
        json={
            "room_id": 1,
            "slot_id": 1,
            "date": "2026-06-15"
        }
    )

    assert response.status_code == 401


def test_invalid_token(client):

    response = client.get(
        "/api/auth/me",
        headers={
            "Authorization": "Bearer invalid_token"
        }
    )

    assert response.status_code == 401