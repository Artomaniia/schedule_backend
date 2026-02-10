from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import schemas, crud

router = APIRouter(prefix="/weekdays", tags=["Weekdays"])


@router.post("", response_model=schemas.WeekdayOut)
def create(payload: schemas.WeekdayCreate, db: Session = Depends(get_db)):
    return crud.create_weekday(db, payload)


@router.get("", response_model=list[schemas.WeekdayOut])
def list_all(db: Session = Depends(get_db)):
    return crud.list_weekdays(db)


@router.get("/{weekday_id}", response_model=schemas.WeekdayOut)
def get_one(weekday_id: int, db: Session = Depends(get_db)):
    return crud.get_weekday(db, weekday_id)


@router.put("/{weekday_id}", response_model=schemas.WeekdayOut)
def update(weekday_id: int, payload: schemas.WeekdayUpdate, db: Session = Depends(get_db)):
    return crud.update_weekday(db, weekday_id, payload)


@router.delete("/{weekday_id}")
def delete(weekday_id: int, db: Session = Depends(get_db)):
    crud.delete_weekday(db, weekday_id)
    return {"status": "ok"}
