from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, Integer
from .db import Base

weekday_disciplines = Table(
    "weekday_disciplines",
    Base.metadata,
    Column("weekday_id", Integer, ForeignKey("weekdays.id", ondelete="CASCADE"), primary_key=True),
    Column("discipline_id", Integer, ForeignKey("disciplines.id", ondelete="CASCADE"), primary_key=True),
)


class Discipline(Base):
    __tablename__ = "disciplines"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    teachers: Mapped[list["Teacher"]] = relationship(back_populates="discipline")
    weekdays: Mapped[list["Weekday"]] = relationship(
        secondary=weekday_disciplines,
        back_populates="disciplines",
    )


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    discipline_id: Mapped[int] = mapped_column(
        ForeignKey("disciplines.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    discipline: Mapped["Discipline"] = relationship(back_populates="teachers")


class Weekday(Base):
    __tablename__ = "weekdays"
    __table_args__ = (UniqueConstraint("name", name="uq_weekdays_name"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # "пн", "вт", ... "вс"
    name: Mapped[str] = mapped_column(String(2), nullable=False)

    disciplines: Mapped[list["Discipline"]] = relationship(
        secondary=weekday_disciplines,
        back_populates="weekdays",
    )
