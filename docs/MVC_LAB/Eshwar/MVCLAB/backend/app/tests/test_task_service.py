import pytest
 
from app.models import User
from app.services.task_service import (TaskService, TaskNotFoundError, NotAuthorizedError)
from app.tests.fakes import FakeTaskRepository, FakeUserRepository
 
def make_service():
    Eshwaryadav = User(id=1, name="Eshwaryadav")
    Bob = User(id=2, name="Bob")
    users = FakeUserRepository([Eshwaryadav, Bob])
    tasks = FakeTaskRepository()
    return TaskService(tasks, users), tasks, Eshwaryadav, Bob
 
def test_list_tasks_returns_only_current_users_tasks():
    service, tasks, Eshwaryadav, Bob = make_service()
    tasks.add("A1", Eshwaryadav.id)
    tasks.add("A2", Eshwaryadav.id)
    tasks.add("B1", Bob.id)
    tasks.add("B2", Bob.id)
    tasks.add("B3", Bob.id)
 
    result = service.list_tasks(Eshwaryadav)
 
    assert len(result) == 2
    assert all(t.owner_id == Eshwaryadav.id for t in result)
 
def test_create_task_strips_whitespace_around_title():
    service, tasks, Eshwaryadav, _ = make_service()
 
    service.create_task("  Read Docs  ", Eshwaryadav)
 
    stored = tasks.all_for_user(Eshwaryadav.id)
    assert len(stored) == 1
    assert stored[0].title == "Read Docs"
 
def test_create_task_rejects_whitespace_only_title():
    service, tasks, Eshwaryadav, _ = make_service()
 
    with pytest.raises(ValueError):
        service.create_task("   ", Eshwaryadav)
 
    assert (tasks.all_for_user(Eshwaryadav.id)) == []
 
def test_get_task_raises_when_id_does_not_exist():
    service, _, Eshwaryadav, _ = make_service()
 
    with pytest.raises(TaskNotFoundError):
        service.get_task(999, Eshwaryadav)
 
def test_get_task_raises_when_user_is_not_owner():
    service, tasks, Eshwaryadav, Bob = make_service()
    bobs_task = tasks.add("Bobs Secret", Bob.id)
 
    with pytest.raises(NotAuthorizedError):
        service.get_task(bobs_task.id, Eshwaryadav)
 
def test_delete_task_raises_when_current_user_is_not_owner():
    service, tasks, Eshwaryadav, Bob = make_service()
    bobs_task = tasks.add("Bobs Task", Bob.id)
 
    with pytest.raises(NotAuthorizedError):
        service.delete_task(bobs_task.id, Eshwaryadav)
 
    assert tasks.find(bobs_task.id) is not None
 
def test_delete_own_task_removes_it_from_repository():
    service, tasks, Eshwaryadav, _ = make_service()
    task = tasks.add("Read Docs", Eshwaryadav.id)
 
    service.delete_task(task.id, Eshwaryadav)
 
    assert tasks.find(task.id) is None
 
 