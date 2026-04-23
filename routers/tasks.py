from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse
from crud import (
    get_task, get_tasks, create_task, update_task, delete_task
)
from utils import get_priority_order, search_in_tasks

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
def create_task_endpoint(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)


@router.get("/", response_model=List[TaskResponse])
def get_tasks_endpoint(
        sort_by: Optional[str] = Query(None),
        order: Optional[str] = Query("asc"),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db)
):
    query = db.query(Task)

    if sort_by:
        if sort_by == "title":
            order_column = Task.title
        elif sort_by == "status":
            order_column = Task.status
        elif sort_by == "created_at":
            order_column = Task.created_at
        elif sort_by == "priority":
            order_column = Task.priority
        else:
            raise HTTPException(status_code=400, detail="Неверное поле для сортировки")

        if order == "desc":
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())

    tasks = query.offset(skip).limit(limit).all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = update_task(db, task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@router.delete("/{task_id}")
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    success = delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"message": "Задача удалена"}


@router.get("/priority/top", response_model=List[TaskResponse])
def get_top_priority_tasks(
        n: int = Query(5, ge=1, le=50),
        db: Session = Depends(get_db)
):
    priority_order = get_priority_order()
    tasks = get_tasks(db)
    tasks.sort(key=lambda t: priority_order[t.priority])
    return tasks[:n]


@router.get("/search/", response_model=List[TaskResponse])
def search_tasks_endpoint(
        q: str,
        db: Session = Depends(get_db)
):
    tasks = get_tasks(db)
    result = search_in_tasks(tasks, q)
    return result
