import pytest
from models import StatusEnum, PriorityEnum


def test_create_task(client):
    response = client.post("/tasks/", json={
        "title": "Новая задача",
        "description": "Описание",
        "status": StatusEnum.waiting.value,
        "priority": PriorityEnum.high.value
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Новая задача"
    assert data["status"] == StatusEnum.waiting.value


def test_create_task_invalid_data(client):
    response = client.post("/tasks/", json={"title": ""})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == ""


def test_create_task_missing_title(client):
    response = client.post("/tasks/", json={"description": "тест"})
    assert response.status_code == 422


def test_get_tasks(client, sample_task):
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["id"] == sample_task.id


def test_get_task_by_id(client, sample_task):
    response = client.get(f"/tasks/{sample_task.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_task.id
    assert data["title"] == sample_task.title


def test_get_nonexistent_task(client):
    response = client.get("/tasks/99999")
    assert response.status_code == 404
    assert "не найдена" in response.json()["detail"]


def test_update_task(client, sample_task):
    response = client.put(f"/tasks/{sample_task.id}", json={
        "status": StatusEnum.completed.value,
        "priority": PriorityEnum.urgent.value
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == StatusEnum.completed.value
    assert data["priority"] == PriorityEnum.urgent.value


def test_delete_task(client, sample_task):
    response = client.delete(f"/tasks/{sample_task.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Задача удалена"

    response = client.get(f"/tasks/{sample_task.id}")
    assert response.status_code == 404


def test_sort_tasks(client):
    client.post("/tasks/", json={"title": "Задача А", "priority": PriorityEnum.low.value})
    client.post("/tasks/", json={"title": "Задача Б", "priority": PriorityEnum.high.value})

    response = client.get("/tasks/?sort_by=title&order=asc")
    assert response.status_code == 200
    tasks = response.json()
    titles = [t["title"] for t in tasks]
    assert titles == sorted(titles)

    response = client.get("/tasks/?sort_by=priority")
    assert response.status_code == 200


def test_sort_invalid_field(client):
    response = client.get("/tasks/?sort_by=invalid_field")
    assert response.status_code == 400


def test_search_tasks(client, sample_task):
    response = client.get(f"/tasks/search/?q={sample_task.title[:3]}")
    assert response.status_code == 200
    data = response.json()
    assert any(task["id"] == sample_task.id for task in data)


def test_top_priority_tasks(client):
    client.post("/tasks/", json={"title": "Срочная", "priority": PriorityEnum.urgent.value})
    client.post("/tasks/", json={"title": "Высокая", "priority": PriorityEnum.high.value})
    client.post("/tasks/", json={"title": "Низкая", "priority": PriorityEnum.low.value})

    response = client.get("/tasks/priority/top?n=2")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2


def test_pagination(client):
    for i in range(10):
        client.post("/tasks/", json={"title": f"Task {i}"})

    response = client.get("/tasks/?skip=0&limit=5")
    assert response.status_code == 200
    assert len(response.json()) == 5

    response = client.get("/tasks/?skip=5&limit=5")
    assert len(response.json()) == 5


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Task Manager API" in response.json()["message"]


def test_update_task_partial_data(client, sample_task):
    response = client.put(f"/tasks/{sample_task.id}", json={
        "title": "Обновление только одного поля"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Обновление только одного поля"
    assert data["description"] == sample_task.description


def test_get_tasks_with_pagination_and_sort(client):
    for i in range(15):
        client.post("/tasks/", json={
            "title": f"Task {i}",
            "priority": PriorityEnum.high.value if i % 2 == 0 else PriorityEnum.low.value
        })

    response = client.get("/tasks/?sort_by=title&order=asc&skip=5&limit=5")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 5


def test_search_no_results(client):
    response = client.get("/tasks/search/?q=xyz123nonexistent")
    assert response.status_code == 200
    assert response.json() == []


def test_top_priority_with_more_tasks_than_exist(client):
    tasks = client.get("/tasks/").json()
    for task in tasks:
        client.delete(f"/tasks/{task['id']}")

    for i in range(3):
        client.post("/tasks/", json={"title": f"Task {i}"})

    response = client.get("/tasks/priority/top?n=10")
    assert response.status_code == 200
    assert len(response.json()) == 3
