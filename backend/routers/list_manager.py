from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas

router = APIRouter(prefix="/lists", tags=["lists"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ListEntry, status_code=status.HTTP_201_CREATED)
def create_list_entry(entry_in: schemas.ListEntryCreate, db: Session = Depends(get_db)):
    db_e = models.ListEntry(**entry_in.dict())
    db.add(db_e)
    db.commit()
    db.refresh(db_e)
    return db_e

@router.get("/", response_model=list[schemas.ListEntry])
def list_entries(
    profile_id: int = Query(None),
    type: schemas.ListTypeEnum = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    q = db.query(models.ListEntry)
    if profile_id is not None:
        q = q.filter(models.ListEntry.profile_id == profile_id)
    if type is not None:
        q = q.filter(models.ListEntry.type == type)
    return q.offset(skip).limit(limit).all()

@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list_entry(entry_id: int, db: Session = Depends(get_db)):
    db_e = db.query(models.ListEntry).get(entry_id)
    if not db_e:
        raise HTTPException(status_code=404, detail="List entry not found")
    db.delete(db_e)
    db.commit()
    return
