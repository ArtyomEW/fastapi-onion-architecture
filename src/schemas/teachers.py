from .dependencies_for_schemas import BaseSchema
from pydantic import Field, BaseModel
from datetime import datetime
from typing import Literal
from uuid import UUID


class STeacherRequiredFields(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = Field(default=None)
    login: str


class STeachers(BaseSchema, STeacherRequiredFields):
    hashed_password: str
    is_role: str
    is_active: int
    created_on: datetime
    updated_on: datetime


class STeachersSubjects(BaseModel):
    subjects: list[UUID]


class STeachersGroups(BaseModel):
    groups: list[UUID]


class SRoleStudents(BaseModel):
    is_role: Literal["professor", "associate_professor",
                     "senior_lecturer", "assistant"] = "senior_lecturer"


class STeacherAdd(STeacherRequiredFields):
    hashed_password: str


class STeachersEdit(STeacherRequiredFields, SRoleStudents):
    pass
