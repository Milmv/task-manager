import pytest
from crud import create_task, get_task, update_task, delete_task, get_tasks
from schemas import TaskCreate, TaskUpdate
from models import StatusEnum, PriorityEnum


def test_crud_operations(db_session):
    task_create = TaskCreate(
        title="Интеграционная задача",
        description="Тест CRUD операций",
        status=StatusEnum.waiting,
        priority=PriorityEnum.high
    )
    task = create_task(db_session, task_create)
    assert task.id is not None

    fetched = get_task(db_session, task.id)
    assert fetched.title == "Интеграционная задача"

    task_update = TaskUpdate(status=StatusEnum.completed)
    updated = update_task(db_session, task.id, task_update)
    assert updated.status == StatusEnum.completed

    result = delete_task(db_session, task.id)
    assert result is True

    deleted = get_task(db_session, task.id)
    assert deleted is None


def test_get_tasks_pagination(db_session):
    for i in range(50):
        task = TaskCreate(title=f"Task {i}")
        create_task(db_session, task)

    tasks = get_tasks(db_session, skip=0, limit=10)
    assert len(tasks) == 10

    tasks = get_tasks(db_session, skip=40, limit=20)
    assert len(tasks) == 10
