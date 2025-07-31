from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
import schemas

# ensure tables exist
Base.metadata.create_all(bind=engine)


router = APIRouter(prefix="/lists", tags=["lists"])


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ListEntry, status_code=status.HTTP_201_CREATED)
def create_list(list_in: schemas.ListEntryCreate, db: Session = Depends(get_db)):
    db_list = models.ListEntry(**list_in.model_dump())
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

@router.get("/", response_model=list[schemas.ListEntry])
def list_entries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ListEntry).offset(skip).limit(limit).all()

@router.get("/{list_id}", response_model=schemas.ListEntry)
def get_list_entry(list_id: int, db: Session = Depends(get_db)):
    db_list = db.query(models.ListEntry).get(list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="List entry not found")
    return db_list

@router.put("/{list_id}", response_model=schemas.ListEntry)
def update_list_entry(
    list_id: int, list_in: schemas.ListEntryCreate, db: Session = Depends(get_db)
):
    db_list = db.query(models.ListEntry).get(list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="List entry not found")
    for key, val in list_in.model_dump().items():
        setattr(db_list, key, val)
    db.commit()
    db.refresh(db_list)
    return db_list

@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list_entry(list_id: int, db: Session = Depends(get_db)):
    db_list = db.query(models.ListEntry).get(list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="List entry not found")
    db.delete(db_list)
    db.commit()
    return {"detail": "List entry deleted successfully"}
