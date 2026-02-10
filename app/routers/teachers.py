from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import schemas, crud

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.post("", response_model=schemas.TeacherOut)
def create(payload: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return crud.create_teacher(db, payload)


@router.get("", response_model=list[schemas.TeacherOut])
def list_all(db: Session = Depends(get_db)):
    return crud.list_teachers(db)


@router.get("/{teacher_id}", response_model=schemas.TeacherOut)
def get_one(teacher_id: int, db: Session = Depends(get_db)):
    return crud.get_teacher(db, teacher_id)


@router.put("/{teacher_id}", response_model=schemas.TeacherOut)
def update(teacher_id: int, payload: schemas.TeacherUpdate, db: Session = Depends(get_db)):
    return crud.update_teacher(db, teacher_id, payload)


@router.delete("/{teacher_id}")
def delete(teacher_id: int, db: Session = Depends(get_db)):
    crud.delete_teacher(db, teacher_id)
    return {"status": "ok"}
