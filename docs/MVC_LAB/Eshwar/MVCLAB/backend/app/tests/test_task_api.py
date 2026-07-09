def test_get_tasks_empty_returns_200_and_empty_list(client):
    """GET /tasks/ with no tasks yet returns 200 and []."""
    ...
 
def test_post_task_returns_201_with_created_task(client, eshwaryadav):
    """
    POST /tasks/ with {"title": "read docs"} returns 201.
    Body has an id, title == "read docs".
    Hint: r = client.post("/tasks/", json={"title": "read docs"})
    """
    ...
 
def test_post_task_with_empty_title_returns_422(client):
   """
   pydantic min_length=1 rejects an empty title before the service is called.
   Status: 422.
   """
   ...
 
def test_get_task_by_id_returns_the_task(client):
    """
    POST creates a task, then GET /tasks/{id} returns the same task with 200.
    Hint: pull id out of the POST response body.
    """
    ...
 
def test_delete_own_task_returns_204_then_get_returns_404(client):
    """
    create a task, DELETE it (expect 204), then GET the same id (expect 404).
    """
    ...
 