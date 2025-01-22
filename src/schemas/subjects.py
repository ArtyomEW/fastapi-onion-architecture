from .dependencies_for_schemas import BaseSchema
from pydantic import Field, BaseModel


class SSubjects(BaseSchema):
    name: str
    groups: list | None = Field(default=None)
    teachers: list | None = Field(default=None)


class SSubjectsAdd(BaseModel):
    name: str
    groups: list | None = Field(default=None)
    teachers: list | None = Field(default=None)
