from fastapi import FastAPI
from src.utils.db import Base,engine
from src.tasks.models import TaskModal

Base.metadata.create_all(bind=engine)

app=FastAPI(title="Task Management API",description="This is a task management API built with FastAPI and SQLAlchemy.")
@app.get("/")
def home():
    return {"message": "Hello World"}

