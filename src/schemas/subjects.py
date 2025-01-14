from .dependencies_for_schemas import BaseSchema
from pydantic import Field


class SSubjects(BaseSchema):
    id: int
    name: str
    groups: list | None = Field(default=None)
    teachers: list | None = Field(default=None)
