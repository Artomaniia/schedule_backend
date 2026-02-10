from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import schemas, crud

router = APIRouter(prefix="/disciplines", tags=["Disciplines"])


@router.post("", response_model=schemas.DisciplineOut)
def create(payload: schemas.DisciplineCreate, db: Session = Depends(get_db)):
    return crud.create_discipline(db, payload)


@router.get("", response_model=list[schemas.DisciplineOut])
def list_all(db: Session = Depends(get_db)):
    return crud.list_disciplines(db)


@router.get("/{discipline_id}", response_model=schemas.DisciplineOut)
def get_one(discipline_id: int, db: Session = Depends(get_db)):
    return crud.get_discipline(db, discipline_id)


@router.put("/{discipline_id}", response_model=schemas.DisciplineOut)
def update(discipline_id: int, payload: schemas.DisciplineUpdate, db: Session = Depends(get_db)):
    return crud.update_discipline(db, discipline_id, payload)


@router.delete("/{discipline_id}")
def delete(discipline_id: int, db: Session = Depends(get_db)):
    crud.delete_discipline(db, discipline_id)
    return {"status": "ok"}
