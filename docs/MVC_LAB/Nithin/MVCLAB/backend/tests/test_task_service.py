import pytest
from app.models import User
from app.services.task_service import (TaskService, TaskNotFoundError, NotAuthorizedError)
from tests.fakes import FakeTaskRepository, FakeUserRepository

def make_service():
    nithin = User(id=1, name="Nithin", password_hash="password123")
    doe = User(id=2, name="Doe", password_hash="password123")
    tasks = FakeTaskRepository()
    users = FakeUserRepository([nithin, doe])
    service = TaskService(tasks, users)
    return service, tasks, nithin, doe

def test_list_tasks_return_only_current_user_tasks():
    service, tasks, nithin, doe = make_service()
    tasks.add("Nithin Task 1", nithin.id)
    tasks.add("Doe Task 2", doe.id)
    tasks.add("Nithin Task 3", nithin.id)

    user_tasks = service.list_tasks(nithin)

    assert len(user_tasks) == 2
    assert all(task.owner_id == nithin.id for task in user_tasks)

def test_create_task_strips_whitespace_around_title():
    service, tasks, nithin, _ = make_service()
    service.create_task(" Read Docs ", nithin)
    user_tasks = tasks.all_for_user(nithin.id)

    assert len(user_tasks) == 1
    assert user_tasks[0].title == "Read Docs"

def test_create_task_rejects_whitespace_title():
    service,tasks, nithin, doe = make_service()
    with pytest.raises(ValueError):
        service.create_task("  ", nithin)

def test_get_task_raises_when_id_does_not_exist():
    service, tasks, nithin, doe = make_service()
    with pytest.raises(TaskNotFoundError):
        service.get_task(999, nithin)

def test_get_task_raises_when_current_user_is_not_owner():
    service, tasks, nithin, doe = make_service()
    bob_task = tasks.add("Bob's Task", doe.id)
    with pytest.raises(NotAuthorizedError):
        service.get_task(bob_task.id, nithin)

def test_delete_task_raises_when_current_user_is_not_owner():
    service, tasks, nithin, doe = make_service()
    bob_task = tasks.add("Bob's Task", doe.id)
    with pytest.raises(NotAuthorizedError):
        service.get_task(bob_task.id, nithin)
    assert tasks.find(bob_task.id) is not None  # Task should still exist

def test_delete_task_removes_task_removes_it_from_repository():
    service, tasks, nithin, doe = make_service()
    task = service.create_task("My Task", nithin)
    service.delete_task(task.id, nithin)
    assert tasks.find(task.id) is None                   