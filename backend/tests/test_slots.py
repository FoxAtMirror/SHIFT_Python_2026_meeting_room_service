def test_get_slots_for_nonexistent_room(client):

    response = client.get(
        "/api/slots/room/999999"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

def get_admin_token(
    client
):

    client.post(
        "/api/auth/register",
        json={
            "login": "admin",
            "password": "12345"
        }
    )

    token = client.post(
        "/api/auth/login",
        data={
            "username": "admin",
            "password": "12345"
        }
    ).json()["access_token"]

    from app.db.test_database import (
        TestingSessionLocal
    )
    from app.db.models import User

    db = TestingSessionLocal()

    admin = (
        db.query(User)
        .filter(
            User.login == "admin"
        )
        .first()
    )

    admin.role = "admin"

    db.commit()

    db.close()

    return token


def test_cannot_create_overlapping_slots(
    client
):

    token = get_admin_token(
        client
    )

    room_response = client.post(
        "/api/rooms",
        json={
            "name": "Test Room"
        },
        headers={
            "Authorization":
                f"Bearer {token}"
        }
    )

    room_id = (
        room_response.json()["id"]
    )

    first_slot = client.post(
        "/api/slots",
        json={
            "room_id": room_id,
            "start_time": "09:00:00",
            "end_time": "11:00:00"
        },
        headers={
            "Authorization":
                f"Bearer {token}"
        }
    )

    assert first_slot.status_code == 200

    second_slot = client.post(
        "/api/slots",
        json={
            "room_id": room_id,
            "start_time": "10:00:00",
            "end_time": "12:00:00"
        },
        headers={
            "Authorization":
                f"Bearer {token}"
        }
    )

    assert second_slot.status_code == 400

    assert (
        second_slot.json()["detail"]
        ==
        "Slot overlaps with existing slot"
    )