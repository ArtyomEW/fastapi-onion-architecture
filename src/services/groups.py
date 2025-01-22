from sqlalchemy.exc import IntegrityError
from utils.unitofwork import UnitOfWork
from core.exceptions import MyException
from schemas.groups import SGroupsAdd
from models.groups import Groups
from uuid import UUID
import importlib


class GroupsService:

    @staticmethod
    async def __get_students(uow: UnitOfWork, students_uuid: list[UUID]) -> list:
        """
        Получаем студентов с
        помощью сервиса StudentsService
        """
        module = importlib.import_module("services.students")
        list_students = []
        for uuid in students_uuid:
            students = await module.StudentsService().get_students_with_filter_uuid(uow, uuid)
            if not students:
                raise MyException(status_code=409, message="Этого студента не существует. "
                                                           "Добавьте студента в базу данных")
            else:
                list_students.append(students)
        return list_students

    @staticmethod
    async def __get_subjects(uow: UnitOfWork, subjects_uuid: list[UUID]) -> list:
        """
        Получаем предметы с
        помощью сервиса SubjectsService
        """
        module = importlib.import_module("services.subjects")
        list_subjects = []
        for subject in subjects_uuid:
            subjects = await module.SubjectsService().get_subjects_with_filter_uuid(uow, subject)
            if not subjects:
                raise MyException(status_code=409, message="Этого предмета не существует. "
                                                           "Добавьте предмет в базу данных")
            else:
                list_subjects.append(subject)
        return list_subjects

    @staticmethod
    async def __get_teachers(uow: UnitOfWork, teachers_uuid: list[UUID]) -> list:
        """
        Получаем преподавателей с
        помощью сервиса TeachersService
        """
        module = importlib.import_module("services.teachers")
        list_teachers = []
        for teacher in teachers_uuid:
            teachers = await module.TeachersService().get_teachers_with_filter_uuid(uow, teacher)
            if not teachers:
                raise MyException(status_code=409, message="Этого преподавателя не существует. "
                                                           "Добавьте преподавателя в базу данных")
            else:
                list_teachers.append(teacher)
        return list_teachers

    @staticmethod
    def __are_there_any_letters_in_the_group_number_etc(number_group: str) -> bool:
        """
        Проверяем есть ли в номере
        группы буквы или прочее символы
        """
        for v in number_group:
            if not v.isdigit():
                return False
        return True

    @classmethod
    async def add_groups(cls, uow: UnitOfWork, groups_schema: SGroupsAdd | dict):
        """
        Добавляем группу со студентами, предметами, преподавателями.
        Используя их сервисы.
        StudentsService, SubjectsService, TeachersService
        """
        if type(groups_schema) is not dict:
            groups_schema = groups_schema.model_dump()

        number_group = groups_schema.get('number_group')
        students_uuid = groups_schema.get('students')
        subjects_uuid = groups_schema.get('subjects')
        teachers_uuid = groups_schema.get('teachers')
        del groups_schema

        res: bool = cls.__are_there_any_letters_in_the_group_number_etc(number_group)

        if not res:
            raise MyException(status_code=409, message="Номер группы должен "
                                                       "состоять только из цифр")

        groups = Groups(number_group=number_group)
        if students_uuid:
            students: list = await cls.__get_students(uow, students_uuid)
            groups.students.extend(students)
        if subjects_uuid:
            subjects: list = await cls.__get_subjects(uow, subjects_uuid)
            groups.subjects.extend(subjects)
        if teachers_uuid:
            teachers: list = await cls.__get_teachers(uow, teachers_uuid)
            groups.teachers.extend(teachers)

        async with uow:
            uow.session.add(groups)
            try:
                await uow.commit()
                return groups.uuid
            except IntegrityError:
                await uow.session.rollback()
                raise MyException(status_code=505, message="Исключение произошло в add_groups."
                                                           "Возможно вы добавляете существующую группу")

    @classmethod
    async def get_groups_with_filter(cls, uow: UnitOfWork, number_group: str):
        """
        Вывод конкретной группы
        """
        res: bool = cls.__are_there_any_letters_in_the_group_number_etc(number_group)
        if not res:
            raise MyException(status_code=409, message="Номер группы должен "
                                                       "состоять только из цифр")
        async with uow:
            try:
                groups = await uow.groups.find_all_with_filer({"number_group": number_group})
                return groups[0]
            except Exception as e:
                raise MyException(status_code=505, message=f"Исключение в get_groups_with_filter - {e}")

    @staticmethod
    async def get_only_groups(uow: UnitOfWork):
        """
        Вывод всех групп
        """
        try:
            async with uow:
                groups = await uow.groups.find_all()
                return groups
        except Exception as e:
            raise MyException(status_code=505, message=f"Исключение в get_only_groups - {e}")
