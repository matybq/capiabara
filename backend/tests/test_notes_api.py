def _create_user(client, name="Alice"):
    response = client.post("/users/", json={"name": name})
    assert response.status_code == 201
    return response.json()


def test_create_note_returns_201(client):
    user = _create_user(client)
    response = client.post("/notes/", json={"user_id": user["id"], "content": "Hello", "title": "Greet"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["user_id"] == user["id"]
    assert data["content"] == "Hello"
    assert data["title"] == "Greet"
    assert data["is_deleted"] is False


def test_list_notes_scoped_by_user(client):
    user_a = _create_user(client, "Alice")
    user_b = _create_user(client, "Bob")

    client.post("/notes/", json={"user_id": user_a["id"], "content": "Note A1"})
    client.post("/notes/", json={"user_id": user_a["id"], "content": "Note A2"})
    client.post("/notes/", json={"user_id": user_b["id"], "content": "Note B1"})

    notes_a = client.get("/notes/", params={"user_id": user_a["id"]}).json()
    notes_b = client.get("/notes/", params={"user_id": user_b["id"]}).json()

    assert len(notes_a) == 2
    assert all(n["user_id"] == user_a["id"] for n in notes_a)

    assert len(notes_b) == 1
    assert notes_b[0]["user_id"] == user_b["id"]


def test_get_note_returns_created_note(client):
    user = _create_user(client)
    created = client.post("/notes/", json={"user_id": user["id"], "content": "My note"}).json()
    response = client.get(f"/notes/{created['id']}")
    assert response.status_code == 200
    assert response.json()["content"] == "My note"


def test_delete_note_soft_deletes(client):
    user = _create_user(client)
    created = client.post("/notes/", json={"user_id": user["id"], "content": "To delete"}).json()
    note_id = created["id"]

    client.delete(f"/notes/{note_id}")

    list_response = client.get("/notes/", params={"user_id": user["id"]})
    ids = [n["id"] for n in list_response.json()]
    assert note_id not in ids

    get_response = client.get(f"/notes/{note_id}")
    assert get_response.status_code == 404


def test_create_note_with_nonexistent_user_returns_404(client):
    response = client.post("/notes/", json={"user_id": 99999, "content": "Ghost note"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_list_notes_rejects_non_integer_user_id(client):
    """GET /notes/?user_id=abc must return 422 — user_id must be an integer."""
    response = client.get("/notes/", params={"user_id": "abc"})
    assert response.status_code == 422
