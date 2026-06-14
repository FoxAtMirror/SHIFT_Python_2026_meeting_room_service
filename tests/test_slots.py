def test_get_slots_for_nonexistent_room(client):

    response = client.get(
        "/api/slots/room/999999"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )