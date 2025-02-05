from repositories.subjects import SubjectsRepository
from repositories.teachers import TeachersRepository
from repositories.students import StudentsRepository
from repositories.groups import GroupsRepository
from repositories.files import FilesRepository
from db.db import async_session_maker
from abc import ABC, abstractmethod
from typing import Type


# https://github1s.com/cosmicpython/code/tree/chapter_06_uow
class IUnitOfWork(ABC):
    students: Type[StudentsRepository]
    teachers: Type[TeachersRepository]
    subjects: Type[SubjectsRepository]
    groups: Type[GroupsRepository]
    files: Type[FilesRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:

    service_session = async_session_maker()

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.students = StudentsRepository(self.session)
        self.groups = GroupsRepository(self.session)
        self.subjects = SubjectsRepository(self.session)
        self.teachers = TeachersRepository(self.session)
        self.files = FilesRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
