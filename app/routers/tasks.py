from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def log_activity(db, user_id, action, entity_type, entity_id):
    log = models.ActivityLog(user_id=user_id, action=action, entity_type=entity_type, entity_id=entity_id)
    db.add(log)
    db.commit()

@router.post("/", response_model=schemas.TaskOut)
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = models.Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    log_activity(db, current_user.id, "created", "task", task.id)
    return task

@router.get("/project/{project_id}", response_model=list[schemas.TaskOut])
def get_tasks(project_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, data: schemas.TaskUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    log_activity(db, current_user.id, "updated", "task", task.id)
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    log_activity(db, current_user.id, "deleted", "task", task_id)
    return {"message": "Task deleted"}