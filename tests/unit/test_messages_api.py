def test_list_messages_empty(client):
    resp = client.get("/api/v1/messages")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_message(client):
    resp = client.post("/api/v1/messages", json={"text": "hello"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["text"] == "hello"

    list_resp = client.get("/api/v1/messages")
    assert list_resp.status_code == 200
    assert len(list_resp.get_json()) == 1
