from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
import schemas


# ensure tables exist
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/logs", tags=["logs"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{log_id}", response_model=schemas.LogEntry)
def get_log_entry(log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(models.LogEntry).get(log_id)
    if not db_log:
        raise HTTPException(status_code=404, detail="Log entry not found")
    return db_log
