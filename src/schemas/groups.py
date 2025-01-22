from .dependencies_for_schemas import BaseSchema
from pydantic import Field, BaseModel
from uuid import UUID


class SGroups(BaseSchema):
    number_group: str
    subjects: list[str] | None = None
    teachers: list[str] | None = None
    students: list[str] | None = None


class SGroupsAdd(BaseModel):
    number_group: str
    students: list[UUID] | None = Field(default=None, description="There should be uuid of students here")
    subjects: list[UUID] | None = Field(default=None, description="There should be uuid of subjects here")
    teachers: list[UUID] | None = Field(default=None, description="There should be uuid of teachers here")
