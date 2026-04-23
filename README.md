### Запуск

1) python -m venv venv
2) venv\Scripts\activate или source venv/bin/activate
3) pip install -r requirements.txt
4) uvicorn main:app --reload

## О запросах

1) сваггер - http://localhost:8000/docs
2) все задачи - http://localhost:8000/tasks/
3) получить задачу по id - http://localhost:8000/tasks/{id}
4) получить топ - http://localhost:8000/tasks/priority/top?n={число}
5) поиск задачи - http://localhost:8000/tasks/search/?q={текст}
6) сортировка - http://localhost:8000/tasks/?sort_by={title/status/priority/created_at}&order={asc/desc}
   или http://localhost:8000/tasks/?sort_by={title/status/priority/created_at}

7) добавить задачу -

```curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": {текст},
    "description": {текст},
    "status": {статус},
    "priority": {приоритет}
  }'
```

8) удалить задачу -
   ``` curl -X DELETE "http://localhost:8000/tasks/{id}"  ```
9) обновить задачу -

  ``` curl -X PUT "http://localhost:8000/tasks/1" \
   -H "Content-Type: application/json" \
   -d '{
   "status": {статус},
   "priority": {приоритет}
   }'```
