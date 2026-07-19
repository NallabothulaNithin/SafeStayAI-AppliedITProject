import pytest
from app.models import User
from app.services.task_service import (
    TaskService, TaskNotFoundError, NotAuthorizedError
)
from tests.fakes import FakeTaskRepository, FakeUserRepository

# Add these temporary definitions right below your imports if they aren't in your app service yet
class TaskNotFoundError(Exception):
    pass

class NotAuthorizedError(Exception):
    pass

def make_service():
    """Build a TaskService with fresh fakes and two known users."""
    alice = User(id=1, name="Alice")
    bob = User(id=2, name="Bob")
    tasks = FakeTaskRepository()
    users = FakeUserRepository([alice, bob])
    return TaskService(tasks, users), tasks, alice, bob

def test_list_tasks_returns_only_current_users_tasks():
    """Alice has 2 tasks, Bob has 3. list_tasks(alice) returns exactly 2."""
    # Arrange
    service, tasks, alice, bob = make_service()
    tasks.add(title="Alice task 1", owner_id=alice.id)
    tasks.add(title="Alice task 2", owner_id=alice.id)
    tasks.add(title="Bob task 1", owner_id=bob.id)
    tasks.add(title="Bob task 2", owner_id=bob.id)
    tasks.add(title="Bob task 3", owner_id=bob.id)

    # Act
    result = service.list_tasks(alice)

    # Assert
    assert len(result) == 2
    assert all(t.owner_id == alice.id for t in result)

def test_create_task_strips_whitespace_around_title():
    """create_task('read docs ', alice) stores title 'read docs'."""
    # Arrange
    service, tasks, alice, _ = make_service()

    # Act
    service.create_task(title="read docs ", current_user=alice)

    # Assert
    alice_tasks = tasks.all_for_user(alice.id)
    assert len(alice_tasks) == 1
    assert alice_tasks[0].title == "read docs"

def test_create_task_rejects_whitespace_only_title():
    """create_task(' ', alice) raises ValueError; nothing is stored."""
    # Arrange
    service, tasks, alice, _ = make_service()

    # Act & Assert
    with pytest.raises(ValueError):
        service.create_task(title=" ", current_user=alice)
    
    assert len(tasks.all_for_user(alice.id)) == 0

def test_get_task_raises_when_id_does_not_exist():
    """service.get_task(999, alice) raises TaskNotFoundError."""
    # Arrange
    service, _, alice, _ = make_service()

    # Act & Assert
    with pytest.raises(TaskNotFoundError):
        service.get_task(task_id=999, current_user=alice)

def test_get_task_raises_when_current_user_is_not_owner():
    """Bob creates a task. Alice calls get_task(bob_task.id, alice) -> NotAuthorizedError."""
    # Arrange
    service, tasks, alice, bob = make_service()
    bob_task = tasks.add(title="Bob's private task", owner_id=bob.id)

    # Act & Assert
    with pytest.raises(NotAuthorizedError):
        service.get_task(task_id=bob_task.id, current_user=alice)

def test_delete_task_raises_when_current_user_is_not_owner():
    """Bob creates a task. Alice tries to delete it -> NotAuthorizedError."""
    # Arrange
    service, tasks, alice, bob = make_service()
    bob_task = tasks.add(title="Bob's persistent task", owner_id=bob.id)

    # Act & Assert
    with pytest.raises(NotAuthorizedError):
        service.delete_task(task_id=bob_task.id, current_user=alice)
    
    # Verify the task is STILL PRESENT in the repository afterwards
    assert tasks.find(bob_task.id) is not None

def test_delete_own_task_removes_it_from_repository():
    """Alice creates a task, then deletes it. tasks.find(id) returns None."""
    # Arrange
    service, tasks, alice, _ = make_service()
    alice_task = tasks.add(title="Alice's fragile task", owner_id=alice.id)

    # Act
    service.delete_task(task_id=alice_task.id, current_user=alice)

    # Assert
    assert tasks.find(alice_task.id) is None