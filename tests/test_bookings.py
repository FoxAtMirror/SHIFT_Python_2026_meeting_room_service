from datetime import date


def get_token(client, login, password):

    client.post(
        "/auth/register",
        json={
            "login": login,
            "password": password
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": login,
            "password": password
        }
    )

    return response.json()["access_token"]


def test_create_booking(client):

    token = get_token(
        client,
        "booking_user",
        "12345"
    )

    room = client.post(
        "/rooms",
        json={
            "name": "Room A"
        }
    )

    room_id = room.json()["id"]

    slot = client.post(
        "/slots",
        json={
            "room_id": room_id,
            "start_time": "09:00",
            "end_time": "11:00"
        }
    )

    slot_id = slot.json()["id"]

    response = client.post(
        "/bookings",
        json={
            "room_id": room_id,
            "slot_id": slot_id,
            "date": "2026-06-20"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["room_id"] == room_id
    assert data["slot_id"] == slot_id