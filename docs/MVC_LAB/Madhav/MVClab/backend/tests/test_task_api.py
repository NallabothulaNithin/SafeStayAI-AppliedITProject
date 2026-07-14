from app.models import Task
 
 
def test_get_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []
 
 
def test_post_task_returns_201_with_created_task(client):
    response = client.post(
        "/tasks/",
        json={"title": "read docs"}
    )
 
    assert response.status_code == 201
 
    body = response.json()
    assert body["title"] == "read docs"
    assert "id" in body
 
 
def test_post_task_with_empty_title_returns_422(client):
    response = client.post(
        "/tasks/",
        json={"title": ""}
    )
 
    assert response.status_code == 422
 
 
def test_get_task_by_id_returns_the_task(client):
    create = client.post(
        "/tasks/",
        json={"title": "read docs"}
    )
 
    task = create.json()
 
    response = client.get(f"/tasks/{task['id']}")
 
    assert response.status_code == 200
    assert response.json()["id"] == task["id"]
    assert response.json()["title"] == "read docs"
 
 
def test_delete_own_task_returns_204_then_get_returns_404(client):
    create = client.post(
        "/tasks/",
        json={"title": "delete me"}
    )
 
    task = create.json()
 
    delete = client.delete(f"/tasks/{task['id']}")
    assert delete.status_code == 204
 
    response = client.get(f"/tasks/{task['id']}")
    assert response.status_code == 404