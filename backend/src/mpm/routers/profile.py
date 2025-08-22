from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from mpm.database import SessionLocal, engine, Base
import mpm.models as models
import mpm.schemas as schemas
import logging

# ensure tables exist
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/profiles", tags=["profiles"])


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Profile, status_code=status.HTTP_201_CREATED)
def create_profile(profile_in: schemas.ProfileCreate, db: Session = Depends(get_db)):
    db_profile = models.Profile(**profile_in.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.get("/", response_model=list[schemas.Profile])
def list_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    profiles:List[models.Profile] = db.query(models.Profile).offset(skip).limit(limit).all()
    logging.debug("Profiles output: %s", profiles)
    return profiles or []


@router.get("/{profile_id}", response_model=schemas.Profile)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = db.query(models.Profile).get(profile_id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@router.put("/{profile_id}", response_model=schemas.Profile)
def update_profile(
    profile_id: int, profile_in: schemas.ProfileCreate, db: Session = Depends(get_db)
):
    db_profile = db.query(models.Profile).get(profile_id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    for key, val in profile_in.model_dump().items():
        setattr(db_profile, key, val)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = db.query(models.Profile).get(profile_id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    db.delete(db_profile)
    db.commit()
    return
