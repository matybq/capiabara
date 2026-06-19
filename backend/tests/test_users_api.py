def test_create_user_returns_201(client):
    response = client.post("/users/", json={"name": "Alice"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Alice"
    assert data["is_deleted"] is False


def test_list_users_endpoint_removed(client):
    """GET /users/ must no longer exist (removed in phase-1 security hardening)."""
    response = client.get("/users/")
    assert response.status_code == 405


def test_get_user_by_id_endpoint_removed(client):
    """GET /users/{id} must no longer exist — FastAPI returns 404 when no route matches."""
    response = client.get("/users/1")
    assert response.status_code == 404


def test_delete_user_endpoint_removed(client):
    """DELETE /users/{id} must no longer exist — FastAPI returns 404 when no route matches."""
    response = client.delete("/users/1")
    assert response.status_code == 404
