def test_root(client):

    response = client.get("/")

    assert response.status_code == 200

    assert "<html" in response.text.lower()

    assert "Meeting Room Booking Service" in response.text