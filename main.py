from fastapi import FastAPI
from database import engine, Base
from routers import tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager")

app.include_router(tasks.router)


@app.get("/")
def root():
    return {
        "message": "Task Manager API",
        "docs": "http://localhost:8000/docs"
    }
