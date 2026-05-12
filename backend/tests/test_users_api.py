def test_create_user_returns_201(client):
    response = client.post("/users/", json={"name": "Alice"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Alice"
    assert data["is_deleted"] is False


def test_list_users_returns_non_deleted(client):
    client.post("/users/", json={"name": "Alice"})
    client.post("/users/", json={"name": "Bob"})

    response = client.get("/users/")
    assert response.status_code == 200
    names = [u["name"] for u in response.json()]
    assert "Alice" in names
    assert "Bob" in names


def test_get_user_returns_created_user(client):
    created = client.post("/users/", json={"name": "Carol"}).json()
    response = client.get(f"/users/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Carol"


def test_delete_user_soft_deletes(client):
    created = client.post("/users/", json={"name": "Dave"}).json()
    user_id = created["id"]

    client.delete(f"/users/{user_id}")

    list_response = client.get("/users/")
    ids = [u["id"] for u in list_response.json()]
    assert user_id not in ids

    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
