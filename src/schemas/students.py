from datetime import datetime

from .dependencies_for_schemas import BaseSchema
from pydantic import Field


class SStudents(BaseSchema):
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
    group_id: int | None = Field(default=None)
    groups: str | None = Field(default=None)
