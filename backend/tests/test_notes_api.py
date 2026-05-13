def _create_note(client, content="Hello", title=None):
    payload = {"content": content}
    if title is not None:
        payload["title"] = title

    response = client.post("/notes/", json=payload)
    assert response.status_code == 201
    return response.json()


def test_create_note_returns_201(client):
    data = _create_note(client, content="Hello", title="Greet")
    assert data["id"] is not None
    assert data["content"] == "Hello"
    assert data["title"] == "Greet"
    assert data["is_deleted"] is False
    assert data["user_id"] is not None


def test_list_notes_scoped_by_authenticated_user(client):
    created = [
        _create_note(client, content="Note A1"),
        _create_note(client, content="Note A2"),
        _create_note(client, content="Note A3"),
    ]

    response = client.get("/notes/")
    assert response.status_code == 200
    notes = response.json()

    assert len(notes) == 3
    assert {note["id"] for note in notes} == {note["id"] for note in created}
    assert {note["user_id"] for note in notes} == {notes[0]["user_id"]}


def test_get_note_returns_created_note(client):
    created = _create_note(client, content="My note")
    response = client.get(f"/notes/{created['id']}")
    assert response.status_code == 200
    assert response.json()["content"] == "My note"


def test_delete_note_soft_deletes(client):
    created = _create_note(client, content="To delete")
    note_id = created["id"]

    client.delete(f"/notes/{note_id}")

    list_response = client.get("/notes/")
    ids = [n["id"] for n in list_response.json()]
    assert note_id not in ids

    get_response = client.get(f"/notes/{note_id}")
    assert get_response.status_code == 404


def test_list_notes_ignores_unknown_query_params(client):
    _create_note(client, content="Query-safe note")

    response = client.get("/notes/", params={"user_id": "abc"})
    assert response.status_code == 200
    assert len(response.json()) == 1
