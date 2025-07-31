from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas

router = APIRouter(prefix="/logs", tags=["logs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.LogEntry])
def list_logs(
    profile_id: int = Query(None),
    action: str = Query(None),
    status: str = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    q = db.query(models.LogEntry)
    if profile_id is not None:
        q = q.filter(models.LogEntry.profile_id == profile_id)
    if action is not None:
        q = q.filter(models.LogEntry.action == action)
    if status is not None:
        q = q.filter(models.LogEntry.status == status)
    return q.offset(skip).limit(limit).all()
