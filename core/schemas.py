from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime


# StudentClass
class StudentClassBase(BaseModel):
    name: str


class StudentClassCreate(StudentClassBase):
    pass


class StudentClassUpdate(StudentClassBase):
    name: Optional[str] = None


class StudentClass(StudentClassBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# Student
class StudentBase(BaseModel):
    name: str
    student_class_id: int


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    name: Optional[str] = None
    student_class_id: Optional[int] = None


class Student(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
