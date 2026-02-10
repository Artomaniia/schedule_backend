from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from . import models, schemas


# ---------- Disciplines ----------
def create_discipline(db: Session, payload: schemas.DisciplineCreate) -> models.Discipline:
    obj = models.Discipline(name=payload.name.strip())
    db.add(obj)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Дисциплина с таким именем уже существует.")
    db.refresh(obj)
    return obj


def get_discipline(db: Session, discipline_id: int) -> models.Discipline:
    obj = db.get(models.Discipline, discipline_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена.")
    return obj


def list_disciplines(db: Session) -> list[models.Discipline]:
    return list(db.scalars(select(models.Discipline).order_by(models.Discipline.id)))


def update_discipline(db: Session, discipline_id: int, payload: schemas.DisciplineUpdate) -> models.Discipline:
    obj = get_discipline(db, discipline_id)
    if payload.name is not None:
        obj.name = payload.name.strip()
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Дисциплина с таким именем уже существует.")
    db.refresh(obj)
    return obj


def delete_discipline(db: Session, discipline_id: int) -> None:
    obj = get_discipline(db, discipline_id)
    db.delete(obj)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Нельзя удалить дисциплину: на неё ссылаются преподаватели/расписание.",
        )


# ---------- Teachers ----------
def create_teacher(db: Session, payload: schemas.TeacherCreate) -> models.Teacher:
    _ = get_discipline(db, payload.discipline_id)
    obj = models.Teacher(full_name=payload.full_name.strip(), discipline_id=payload.discipline_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_teacher(db: Session, teacher_id: int) -> models.Teacher:
    obj = db.get(models.Teacher, teacher_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Преподаватель не найден.")
    return obj


def list_teachers(db: Session) -> list[models.Teacher]:
    return list(db.scalars(select(models.Teacher).order_by(models.Teacher.id)))


def update_teacher(db: Session, teacher_id: int, payload: schemas.TeacherUpdate) -> models.Teacher:
    obj = get_teacher(db, teacher_id)
    if payload.full_name is not None:
        obj.full_name = payload.full_name.strip()
    if payload.discipline_id is not None:
        _ = get_discipline(db, payload.discipline_id)
        obj.discipline_id = payload.discipline_id
    db.commit()
    db.refresh(obj)
    return obj


def delete_teacher(db: Session, teacher_id: int) -> None:
    obj = get_teacher(db, teacher_id)
    db.delete(obj)
    db.commit()


# ---------- Weekdays ----------
def create_weekday(db: Session, payload: schemas.WeekdayCreate) -> models.Weekday:
    obj = models.Weekday(name=payload.name)
    if payload.discipline_ids:
        disciplines = list(
            db.scalars(select(models.Discipline).where(models.Discipline.id.in_(payload.discipline_ids)))
        )
        found_ids = {d.id for d in disciplines}
        missing = [i for i in payload.discipline_ids if i not in found_ids]
        if missing:
            raise HTTPException(status_code=404, detail=f"Дисциплины не найдены: {missing}")
        obj.disciplines = disciplines

    db.add(obj)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="День недели с таким именем уже существует.")
    db.refresh(obj)
    return obj


def get_weekday(db: Session, weekday_id: int) -> models.Weekday:
    obj = db.get(models.Weekday, weekday_id)
    if not obj:
        raise HTTPException(status_code=404, detail="День недели не найден.")
    return obj


def list_weekdays(db: Session) -> list[models.Weekday]:
    return list(db.scalars(select(models.Weekday).order_by(models.Weekday.id)))


def update_weekday(db: Session, weekday_id: int, payload: schemas.WeekdayUpdate) -> models.Weekday:
    obj = get_weekday(db, weekday_id)

    if payload.name is not None:
        obj.name = payload.name

    if payload.discipline_ids is not None:
        if payload.discipline_ids:
            disciplines = list(
                db.scalars(select(models.Discipline).where(models.Discipline.id.in_(payload.discipline_ids)))
            )
            found_ids = {d.id for d in disciplines}
            missing = [i for i in payload.discipline_ids if i not in found_ids]
            if missing:
                raise HTTPException(status_code=404, detail=f"Дисциплины не найдены: {missing}")
            obj.disciplines = disciplines
        else:
            obj.disciplines = []

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="День недели с таким именем уже существует.")
    db.refresh(obj)
    return obj


def delete_weekday(db: Session, weekday_id: int) -> None:
    obj = get_weekday(db, weekday_id)
    db.delete(obj)
    db.commit()
