from .dependencies_for_schemas import BaseSchema
from pydantic import Field, BaseModel
from datetime import datetime
from typing import Literal
from uuid import UUID


class SStudents(BaseSchema):
    name: str
    surname: str
    father_name: str | None = Field(default=None)
    login: str
    hashed_password: str
    faculty: str | None = Field(default=None)
    is_role: str
    is_active: int
    created_on: datetime
    updated_on: datetime
    group_uuid: UUID | None = Field(default=None)
    groups: str | None = Field(default=None)


class SStudentsAdd(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    surname: str = Field(min_length=2, max_length=50)
    father_name: str | None = Field(default=None, max_length=50)
    login: str = Field(min_length=5, max_length=50)
    hashed_password: str = Field(min_length=8, max_length=50)
    faculty: str | None = Field(default=None, min_length=2, max_length=50)
    is_role: Literal["student", "headman"] = "student"
    groups: str | None = Field(default=None, min_length=1, max_length=50)
