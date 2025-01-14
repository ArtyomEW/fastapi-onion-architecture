from .dependencies_for_schemas import BaseSchema
from pydantic import Field


class SGroups(BaseSchema):
    id: int
    number_group: str
    faculty: str | None = Field(default=None)
    subjects: list | None = Field(default=None)
    teachers: list | None = Field(default=None)
    students: list | None = Field(default=None)
