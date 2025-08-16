from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from mpm.database import SessionLocal
import mpm.models as models
import mpm.schemas as schemas

router = APIRouter(prefix="/templates", tags=["templates"])

# Reuse the same dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Template, status_code=status.HTTP_201_CREATED)
def create_template(template_in: schemas.TemplateCreate, db: Session = Depends(get_db)):
    db_t = models.Template(**template_in.dict())
    db.add(db_t)
    db.commit()
    db.refresh(db_t)
    return db_t

@router.get("/", response_model=list[schemas.Template])
def list_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Template).offset(skip).limit(limit).all()

@router.get("/{template_id}", response_model=schemas.Template)
def get_template(template_id: int, db: Session = Depends(get_db)):
    db_t = db.query(models.Template).get(template_id)
    if not db_t:
        raise HTTPException(status_code=404, detail="Template not found")
    return db_t

@router.put("/{template_id}", response_model=schemas.Template)
def update_template(template_id: int, template_in: schemas.TemplateCreate, db: Session = Depends(get_db)):
    db_t = db.query(models.Template).get(template_id)
    if not db_t:
        raise HTTPException(status_code=404, detail="Template not found")
    for key, val in template_in.dict().items():
        setattr(db_t, key, val)
    db.commit()
    db.refresh(db_t)
    return db_t

@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(template_id: int, db: Session = Depends(get_db)):
    db_t = db.query(models.Template).get(template_id)
    if not db_t:
        raise HTTPException(status_code=404, detail="Template not found")
    db.delete(db_t)
    db.commit()
    return
