def register_and_login(client, username="alice", password="correct-horse"):
    client.post(
        "/api/auth/register",
        json={"username": username, "password": password},
    )
    client.post(
        "/api/auth/login",
        json={"username": username, "password": password},
    )


def test_create_list_update_delete_task(client):
    register_and_login(client)

    resp = client.post("/api/tasks", json={"title": "buy milk"})
    assert resp.status_code == 201
    task_id = resp.get_json()["id"]

    resp = client.get("/api/tasks")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1

    resp = client.patch(f"/api/tasks/{task_id}", json={"done": True})
    assert resp.status_code == 200
    assert resp.get_json()["done"] is True

    resp = client.delete(f"/api/tasks/{task_id}")
    assert resp.status_code == 204

    resp = client.get("/api/tasks")
    assert resp.get_json() == []


def test_cannot_access_another_users_task(client):
    register_and_login(client, "alice", "correct-horse")
    resp = client.post("/api/tasks", json={"title": "alice's task"})
    task_id = resp.get_json()["id"]

    client.post("/api/auth/logout")
    register_and_login(client, "bob", "another-password")

    resp = client.patch(f"/api/tasks/{task_id}", json={"done": True})
    assert resp.status_code == 404
