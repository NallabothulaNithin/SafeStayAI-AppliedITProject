from app.models import Task
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db


def _seed_task(db, title: str, owner_id: int) -> Task:
    t = Task(title=title, owner_id=owner_id)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


def test_list_tasks_does_not_leak_other_users_tasks(
    client, db_session, eshwaryadav, bob
):
    _seed_task(db_session, "Eshwaryadav task", eshwaryadav.id)
    _seed_task(db_session, "Bob task 1", bob.id)
    _seed_task(db_session, "Bob task 2", bob.id)

    response = client.get("/tasks/")

    assert response.status_code == 200

    titles = [task["title"] for task in response.json()]

    assert "Eshwaryadav task" in titles
    assert "Bob task 1" not in titles
    assert "Bob task 2" not in titles


def test_alice_cannot_get_bob_task_by_id(
    client, db_session, bob
):
    bob_task = _seed_task(db_session, "Bob private", bob.id)

    response = client.get(f"/tasks/{bob_task.id}")

    assert response.status_code == 403


def test_alice_cannot_delete_bob_task(
    client, db_session, bob
):
    bob_task = _seed_task(db_session, "Bob private", bob.id)

    response = client.delete(f"/tasks/{bob_task.id}")

    assert response.status_code == 403

    assert db_session.get(Task, bob_task.id) is not None


def test_unauthenticated_request_is_rejected(db_session):
    app.dependency_overrides[get_db] = lambda: db_session

    try:
        raw = TestClient(app)
        response = raw.get("/tasks/")
        assert response.status_code == 401

    finally:
        app.dependency_overrides.clear()