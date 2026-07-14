from fastapi.testclient import TestClient
from app.main import app
from app.models import Task
from app.database import get_db


def _seed_task(db, title: str, owner_id: int) -> Task:
    task = Task(title=title, owner_id=owner_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def test_list_tasks_does_not_leak_other_users_tasks(client, db_session, Nithin, Doe):
    _seed_task(db_session, "Nithin Task", Nithin.id)
    _seed_task(db_session, "Doe Task", Doe.id)

    response = client.get("/api/tasks/")

    assert response.status_code == 200
    titles = [task["title"] for task in response.json()]
    assert "Nithin Task" in titles
    assert "Doe Task" not in titles


def test_nithin_cannot_get_doe_task(client, db_session, Doe):
    task = _seed_task(db_session, "Doe Secret", Doe.id)

    response = client.get(f"/api/tasks/{task.id}")

    assert response.status_code in (403, 404)


def test_nithin_cannot_delete_doe_task(client, db_session, Doe):
    task = _seed_task(db_session, "Doe Secret", Doe.id)

    response = client.delete(f"/api/tasks/{task.id}")

    assert response.status_code == 403
    assert db_session.get(Task, task.id) is not None


def test_unauthenticated_request_is_rejected(db_session):
    app.dependency_overrides[get_db] = lambda: db_session

    raw = TestClient(app)

    response = raw.get("/api/tasks/")

    assert response.status_code == 401

    app.dependency_overrides.clear()