from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

def log_activity(db, user_id, action, entity_type, entity_id):
    log = models.ActivityLog(user_id=user_id, action=action, entity_type=entity_type, entity_id=entity_id)
    db.add(log)
    db.commit()

@router.post("/", response_model=schemas.ProjectOut)
def create_project(data: schemas.ProjectCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    project = models.Project(name=data.name, owner_id=current_user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    log_activity(db, current_user.id, "created", "project", project.id)
    return project

@router.get("/", response_model=list[schemas.ProjectOut])
def get_projects(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(models.Project).filter(models.Project.owner_id == current_user.id).all()

@router.put("/{project_id}", response_model=schemas.ProjectOut)
def update_project(project_id: int, data: schemas.ProjectCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.name = data.name
    db.commit()
    db.refresh(project)
    log_activity(db, current_user.id, "updated", "project", project.id)
    return project

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    log_activity(db, current_user.id, "deleted", "project", project_id)
    return {"message": "Project deleted"}