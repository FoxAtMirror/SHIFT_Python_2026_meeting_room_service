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