from .dependencies_for_schemas import BaseSchema
from pydantic import BaseModel
from uuid import UUID


class Subjects(BaseModel):
    name: str


class SSubjects(Subjects, BaseSchema):
    pass


class SSubjectsEdit(Subjects):
    pass


class SSubjectsGroups(BaseModel):
    groups: list[UUID]


class SSubjectsTeachers(BaseModel):
    teachers: list[UUID]


class SSubjectsAdd(Subjects):
    pass
