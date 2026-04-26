import pytest
from utils import get_priority_order, search_in_tasks
from models import PriorityEnum, StatusEnum, Task


def test_get_priority_order():
    order = get_priority_order()
    assert order[PriorityEnum.urgent] == 1
    assert order[PriorityEnum.high] == 2
    assert order[PriorityEnum.medium] == 3
    assert order[PriorityEnum.low] == 4


def test_search_in_tasks():
    tasks = [
        Task(title="Проект на Python", description="Изучаем Python"),
        Task(title="Урок по FastAPI", description="Создаем API"),
        Task(title="Тестирование", description="Пишем тесты на pytest")
    ]

    result = search_in_tasks(tasks, "python")
    assert len(result) == 1
    assert result[0].title == "Проект на Python"

    result = search_in_tasks(tasks, "API")
    assert len(result) == 1
    assert result[0].title == "Урок по FastAPI"

    result = search_in_tasks(tasks, "pytest")
    assert len(result) == 1
    assert result[0].title == "Тестирование"

    result = search_in_tasks(tasks, "несуществующее")
    assert len(result) == 0
