from locust import HttpUser, task, between
from models import StatusEnum


class TaskUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post("/tasks/", json={
            "title": "Нагрузочная задача",
            "description": "Проверка производительности"
        })
        if response.status_code == 200:
            self.test_task_id = response.json()["id"]
        else:
            self.test_task_id = None

    @task(3)
    def get_tasks(self):
        self.client.get("/tasks/")

    @task(2)
    def create_task(self):
        self.client.post("/tasks/", json={
            "title": "Новая нагрузочная задача",
            "status": StatusEnum.waiting.value
        })

    @task(2)
    def get_single_task(self):
        if self.test_task_id:
            self.client.get(f"/tasks/{self.test_task_id}")

    @task(1)
    def update_task(self):
        if self.test_task_id:
            self.client.put(f"/tasks/{self.test_task_id}", json={
                "status": StatusEnum.in_progress.value
            })

    @task(1)
    def search_tasks(self):
        self.client.get("/tasks/search/?q=тест")

    @task(1)
    def get_top_priority(self):
        self.client.get("/tasks/priority/top?n=10")
