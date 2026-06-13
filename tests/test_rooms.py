def test_get_rooms(client):

    response = client.get("/rooms")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

def test_create_room(client):

    response = client.post(
        "/rooms",
        json={
            "name": "Test Room"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["name"] == "Test Room"