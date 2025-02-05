from .dependencies_for_schemas import BaseSchema
from pydantic import BaseModel
from uuid import UUID


class Groups(BaseModel):
    number_group: str


class SGroups(Groups, BaseSchema):
    pass


class SGroupsSubjects(BaseModel):
    subjects: list[UUID]


class SGroupsStudents(BaseModel):
    students: list[UUID]


class SGroupsTeachers(BaseModel):
    teachers: list[UUID]


class SGroupsAdd(Groups):
    pass


class SGroupsEdit(Groups):
    pass
