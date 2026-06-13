def register_and_get_token(
    client,
    username,
    password
):

    client.post(
        "/auth/register",
        json={
            "login": username,
            "password": password
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )

    return response.json()["access_token"]


def test_user_cannot_delete_foreign_booking(client):

    client.post(
        "/auth/register",
        json={
            "login": "user_a",
            "password": "12345"
        }
    )

    token_a = register_and_get_token(
        client,
        "user_a",
        "12345"
    )

    client.post(
        "/auth/register",
        json={
            "login": "user_b",
            "password": "12345"
        }
    )

    token_b = register_and_get_token(
        client,
        "user_b",
        "12345"
    )


    room_response = client.post(
        "/rooms",
        json={
            "name": "Permission Test Room"
        }
    )

    room_id = room_response.json()["id"]


    slot_response = client.post(
        "/slots",
        json={
            "room_id": room_id,
            "start_time": "09:00",
            "end_time": "11:00"
        }
    )

    slot_id = slot_response.json()["id"]


    booking_response = client.post(
        "/bookings",
        json={
            "room_id": room_id,
            "slot_id": slot_id,
            "date": "2026-06-20"
        },
        headers={
            "Authorization": f"Bearer {token_a}"
        }
    )

    booking_id = booking_response.json()["id"]


    response = client.delete(
        f"/bookings/{booking_id}",
        headers={
            "Authorization": f"Bearer {token_b}"
        }
    )

    assert response.status_code == 403


def test_cannot_book_same_slot_twice(client):

    token = register_and_get_token(
        client,
        "user1",
        "12345"
    )

    room = client.post(
        "/rooms",
        json={
            "name": "Room B"
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

    booking_data = {
        "room_id": room_id,
        "slot_id": slot_id,
        "date": "2026-06-20"
    }

    first = client.post(
        "/bookings",
        json=booking_data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert first.status_code == 200

    second = client.post(
        "/bookings",
        json=booking_data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert second.status_code == 400

    assert (
        second.json()["detail"]
        == "Slot already booked"
    )


def test_get_my_bookings(client):

    token = register_and_get_token(
        client,
        "employee1",
        "12345"
    )

    room = client.post(
        "/rooms",
        json={
            "name": "Room C"
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

    client.post(
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

    response = client.get(
        "/bookings/my",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1