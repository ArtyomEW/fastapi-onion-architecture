from .dependencies_for_schemas import BaseSchema
from pydantic import Field, BaseModel
from datetime import datetime
from typing import Literal
from uuid import UUID


class EnumSchema(BaseModel):
    is_role: Literal["student", "headman"] = "student"


class Student(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    middle_name: str | None = Field(default=None, max_length=50)
    login: str = Field(min_length=5, max_length=50)
    hashed_password: str = Field(min_length=8, max_length=256)
    faculty: str | None = Field(default=None, min_length=2, max_length=50)


class SStudents(Student, BaseSchema):
    is_role: str
    is_active: int
    created_on: datetime
    updated_on: datetime
    group_uuid: UUID | None = Field(default=None)


class SStudentsGroups(BaseModel):
    group: UUID


class SStudentsAdd(Student, EnumSchema):
    pass


class SStudentsEdit(Student, EnumSchema):
    pass
