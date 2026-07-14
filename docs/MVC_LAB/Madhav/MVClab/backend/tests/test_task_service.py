import pytest
from app.models import User
from app.services.task_service import (TaskService, TaskNotFoundError, NotAuthorizedError)
from tests.fakes import FakeTaskRepository, FakeUserRepository
 
def make_service():
    Madhav = User(id=1, name="Madhav", password_hash="password123")
    Ronaldo = User(id=2, name="Ronaldo", password_hash="password123")
    tasks = FakeTaskRepository()
    users = FakeUserRepository([Madhav, Ronaldo])
    service = TaskService(tasks, users)
    return service, tasks, Madhav, Ronaldo
 
def test_list_tasks_return_only_current_user_tasks():
    service, tasks, Madhav, Ronaldo = make_service()
    tasks.add("Madhav Task 1", Madhav.id)
    tasks.add("Ronaldo Task 2", Ronaldo.id)
    tasks.add("Madhav Task 3", Madhav.id)
 
    user_tasks = service.list_tasks(Madhav)
 
    assert len(user_tasks) == 2
    assert all(task.owner_id == Madhav.id for task in user_tasks)
 
def test_create_task_strips_whitespace_around_title():
    service, tasks, Madhav, _ = make_service()
    service.create_task(" Read Docs ", Madhav)
    user_tasks = tasks.all_for_user(Madhav.id)
 
    assert len(user_tasks) == 1
    assert user_tasks[0].title == "Read Docs"
 
def test_create_task_rejects_whitespace_title():
    service,tasks, Madhav, Ronaldo = make_service()
    with pytest.raises(ValueError):
        service.create_task("  ", Madhav)
 
def test_get_task_raises_when_id_Ronaldos_not_exist():
    service, tasks, Madhav, Ronaldo = make_service()
    with pytest.raises(TaskNotFoundError):
        service.get_task(999, Madhav)
 
def test_get_task_raises_when_current_user_is_not_owner():
    service, tasks, Madhav, Ronaldo = make_service()
    Ronaldo_task = tasks.add("Ronaldo's Task", Ronaldo.id)
    with pytest.raises(NotAuthorizedError):
        service.get_task(Ronaldo_task.id, Madhav)
 
def test_delete_task_raises_when_current_user_is_not_owner():
    service, tasks, Madhav, Ronaldo = make_service()
    Ronaldo_task = tasks.add("Ronaldo's Task", Ronaldo.id)
    with pytest.raises(NotAuthorizedError):
        service.get_task(Ronaldo_task.id, Madhav)
    assert tasks.find(Ronaldo_task.id) is not None  # Task should still exist
 
def test_delete_task_removes_task_removes_it_from_repository():
    service, tasks, Madhav, Ronaldo = make_service()
    task = service.create_task("My Task", Madhav)
    service.delete_task(task.id, Madhav)
    assert tasks.find(task.id) is None 