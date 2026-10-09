from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModal
from fastapi import HTTPException
def create_task(body:TaskSchema,db:Session):
    data=body.model_dump()
    new_task=TaskModal(title=data["title"],
                       description=data["description"],
                       is_completed=data["is_completed"])
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created successfully"}

def get_tasks(db:Session):
    tasks=db.query(TaskModal).all()
    return {"status":"All tasks fetched successfully","data":tasks}

def get_one_tasks(task_id:int,db:Session):
    one_task=db.query(TaskModal).get(task_id)

    if not one_task:
        return HTTPException(status_code=404,detail="Task not found")
    return {"status":"Task fetched successfully","data":one_task}

def update_task(body:TaskSchema,task_id:int,db:Session):
    one_task=db.query(TaskModal).get(task_id)
    if not one_task:
        return HTTPException(status_code=404,detail="Task not found")

    # one_task.title=body.title
    # one_task.description=body.description
    # one_task.is_completed=body.is_completed
    body_data=body.model_dump()
    for key,value in body_data.items():
        setattr(one_task,key,value)
    db.add(one_task)
    db.commit()
    db.refresh(one_task)

    return {"status":"Task updated successfully","data":one_task}

def update_task_status(task_id: int, is_completed: bool, db: Session):
    one_task = db.query(TaskModal).filter(TaskModal.id == task_id).first()

    if not one_task:
        raise HTTPException(status_code=404, detail="Task not found")

    one_task.is_completed = is_completed

    db.commit()
    db.refresh(one_task)

    return {
        "status": "Task status updated successfully",
        "data": one_task
}
def delete_task(task_id: int, db: Session):
    one_task=db.query(TaskModal).get(task_id)
    if not one_task:
        return HTTPException(status_code=404,detail="Task not found")


    db.delete(one_task)
    db.commit()
    return {"status":"Task deleted successfully"}
    