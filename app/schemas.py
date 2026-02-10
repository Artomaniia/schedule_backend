from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

WeekdayName = Literal["пн", "вт", "ср", "чт", "пт", "сб", "вс"]


class DisciplineBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class DisciplineCreate(DisciplineBase):
    pass


class DisciplineUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)


class DisciplineOut(DisciplineBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TeacherBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    discipline_id: int


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    discipline_id: Optional[int] = None


class TeacherOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    discipline: DisciplineOut


class WeekdayBase(BaseModel):
    name: WeekdayName


class WeekdayCreate(WeekdayBase):
    discipline_ids: List[int] = Field(default_factory=list)


class WeekdayUpdate(BaseModel):
    name: Optional[WeekdayName] = None
    discipline_ids: Optional[List[int]] = None  # если None — не менять список


class WeekdayOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: WeekdayName
    disciplines: List[DisciplineOut]
