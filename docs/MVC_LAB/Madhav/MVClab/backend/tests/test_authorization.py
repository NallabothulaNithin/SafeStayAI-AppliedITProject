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
 
 
def test_list_tasks_does_not_leak_other_users_tasks(client, db_session, madhav, ronaldo):
    _seed_task(db_session, "Madhav Task", madhav.id)
    _seed_task(db_session, "Ronaldo Task", ronaldo.id)
 
    response = client.get("/tasks/")
 
    assert response.status_code == 200
    titles = [task["title"] for task in response.json()]
    assert "Madhav Task" in titles
    assert "Ronaldo Task" not in titles
 
 
def test_madhav_cannot_get_ronaldo_task(client, db_session, ronaldo):
    task = _seed_task(db_session, "Ronaldo Secret", ronaldo.id)
 
    response = client.get(f"/tasks/{task.id}")
 
    assert response.status_code in (403, 404)
 
 
def test_madhav_cannot_delete_ronaldo_task(client, db_session, ronaldo):
    task = _seed_task(db_session, "Ronaldo Secret", ronaldo.id)
 
    response = client.delete(f"/tasks/{task.id}")
 
    assert response.status_code == 403
    assert db_session.get(Task, task.id) is not None
 
 
def test_unauthenticated_request_is_rejected(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
 
    raw = TestClient(app)
 
    response = raw.get("/tasks/")
 
    assert response.status_code == 401
 
    app.dependency_overrides.clear()