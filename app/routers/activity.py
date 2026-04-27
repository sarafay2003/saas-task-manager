from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.dependencies import require_admin

router = APIRouter(prefix="/activity", tags=["Activity"])

@router.get("/", response_model=list[schemas.ActivityOut])
def get_activity(db: Session = Depends(get_db), current_user=Depends(require_admin)):
    return db.query(models.ActivityLog).order_by(models.ActivityLog.timestamp.desc()).all()