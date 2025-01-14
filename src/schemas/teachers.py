from datetime import datetime

from pydantic import Field
from .dependencies_for_schemas import BaseSchema


class STeachers(BaseSchema):
    id: int
    name: str
    surname: str
    father_name: str | None = Field(default=None)
    login: str
    hashed_password: str
    is_role: str
    is_active: int
    created_on: datetime
    updated_on: datetime
    subjects: list | None = Field(default=None)
    groups: list | None = Field(default=None)
