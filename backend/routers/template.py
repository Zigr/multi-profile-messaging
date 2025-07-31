from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
import schemas

# ensure tables exist
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/templates", tags=["templates"])


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Template, status_code=status.HTTP_201_CREATED)
def create_template(template_in: schemas.TemplateCreate, db: Session = Depends(get_db)):
    db_template = models.Template(**template_in.model_dump())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


@router.get("/", response_model=list[schemas.Template])
def list_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Template).offset(skip).limit(limit).all()

@router.get("/{template_id}", response_model=schemas.Template)
def get_template(template_id: int, db: Session = Depends(get_db)):
    db_template = db.query(models.Template).get(template_id)
    if not db_template:
        raise HTTPException(status_code=404, detail="Template not found")
    return db_template

@router.put("/{template_id}", response_model=schemas.Template)
def update_template(
    template_id: int, template_in: schemas.TemplateCreate, db: Session = Depends(get_db)
):
    db_template = db.query(models.Template).get(template_id)
    if not db_template:
        raise HTTPException(status_code=404, detail="Template not found")
    for key, val in template_in.model_dump ().items():
        setattr(db_template, key, val)
    db.commit()
    db.refresh(db_template)
    return db_template
@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(template_id: int, db: Session = Depends(get_db)):
    db_template = db.query(models.Template).get(template_id)
    if not db_template:
        raise HTTPException(status_code=404, detail="Template not found")
    db.delete(db_template)
    db.commit()
    return
