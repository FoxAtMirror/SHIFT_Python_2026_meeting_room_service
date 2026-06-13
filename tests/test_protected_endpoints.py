def test_me_requires_auth(client):

    response = client.get(
        "/auth/me"
    )

    assert response.status_code == 401


def test_my_bookings_requires_auth(client):

    response = client.get(
        "/bookings/my"
    )

    assert response.status_code == 401