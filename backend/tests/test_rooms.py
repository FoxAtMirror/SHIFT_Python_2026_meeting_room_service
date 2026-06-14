def test_get_rooms(client):

    response = client.get("/api/rooms")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

def test_create_room(
        client,
        admin_token
):

    response = client.post(
        "/api/rooms",
        json={
            "name": "Test Room"
        },
        headers={
        "Authorization":
            f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["name"] == "Test Room"