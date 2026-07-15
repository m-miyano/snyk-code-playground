def register(client, username="alice", password="correct-horse"):
    return client.post(
        "/api/auth/register",
        json={"username": username, "password": password},
    )


def test_register_and_login(client):
    resp = register(client)
    assert resp.status_code == 201

    resp = client.post(
        "/api/auth/login",
        json={"username": "alice", "password": "correct-horse"},
    )
    assert resp.status_code == 200
    assert resp.get_json()["username"] == "alice"


def test_login_rejects_wrong_password(client):
    register(client)
    resp = client.post(
        "/api/auth/login",
        json={"username": "alice", "password": "wrong-password"},
    )
    assert resp.status_code == 401


def test_register_rejects_short_password(client):
    resp = register(client, password="short")
    assert resp.status_code == 400


def test_register_rejects_duplicate_username(client):
    register(client)
    resp = register(client)
    assert resp.status_code == 409


def test_tasks_require_login(client):
    resp = client.get("/api/tasks")
    assert resp.status_code == 401
