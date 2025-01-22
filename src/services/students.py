from core.security import get_password_hash
from sqlalchemy.exc import IntegrityError
from schemas.students import SStudentsAdd
from services.groups import GroupsService
from utils.unitofwork import UnitOfWork
from core.exceptions import MyException
from sqlalchemy.orm import selectinload
from models.teachers import Teachers
from models.students import Students
from models.groups import Groups
from sqlalchemy import select


class StudentsService:
    @staticmethod
    def __convert_lines_to_small_letters(students_schema: dict[str, str]) -> dict:
        """
        Превращаем все строки в
        маленький регистр и делаем
        валидацию этих строк
        """
        data_students = {}
        for key, value in students_schema.items():
            if value and (key != "login" and key != 'hashed_password'):
                for al in value.lower():
                    if not al.isalpha():
                        raise MyException(status_code=409, message=f"Исключение в __convert_lines_to_small_letters. "
                                                                   f"В данных присутствуют прочие символы.")
                data_students[key] = value.lower()
            else:
                if key == 'hashed_password':
                    data_students[key] = get_password_hash(value)
                else:
                    data_students[key] = value
        return data_students

    @classmethod
    async def __add_or_find_and_return_group(cls, uow: UnitOfWork, number_group: str):
        """
        Находим и возвращаем группу.
        Мы используем сервис группы GroupsService()
        """
        group = await GroupsService().get_groups_with_filter(uow, number_group)
        if group:
            return group
        return group

    @classmethod
    async def add_student(cls, uow: UnitOfWork, student_schema: SStudentsAdd):
        """
        Добавляем студента с его группой
        в базу данных или без группы
        Если есть группа, то используем сервис группы
        """
        student_schema: dict = student_schema.model_dump()
        group: str = student_schema.get('groups')
        del student_schema['groups']

        student_schema = cls.__convert_lines_to_small_letters(student_schema)

        is_group = False
        if group is not None:
            group = await cls.__add_or_find_and_return_group(uow, group)
            if not group:
                raise MyException(status_code=409, message="Такой группы не существует")
            is_group = True

        async with uow:
            students = Students(**student_schema)
            if is_group:
                students.groups = group
            uow.session.add(students)
            try:
                await uow.commit()
                return students
            except IntegrityError as e:
                await uow.session.rollback()
                raise MyException(status_code=505, message=f"Исключение произошло в add_student - {e}")

    @staticmethod
    async def get_subjects_and_teachers(uow: UnitOfWork, data: str):
        """
        Выводит студента и его группы,
        его учителей и вывод его предметов
        """
        try:
            stmt = (select(Students).where(Students.uuid == data)
                    .options(selectinload(Students.groups),
                             selectinload(Students.groups).selectinload(Groups.subjects),
                             selectinload(Students.groups).selectinload(Groups.teachers).selectinload(
                                 Teachers.subjects), ))
            res = await uow.service_session.execute(stmt)
            res = res.scalars().all()
            return res
        except Exception as e:
            raise MyException(status_code=505, message=f"Исключение в get_subjects_and_teachers - {e}")

    @staticmethod
    async def get_students_with_filter_uuid(uow: UnitOfWork, uuid: str):
        """
        Находим студента по UUID
        """
        try:
            async with uow:
                students = await uow.students.find_all_with_filer({'uuid': uuid})
                return students[0]
        except Exception as e:
            raise MyException(status_code=409, message=f"Исключение в get_students_with_filter_uuid - {e}. "
                                                       f"Возможно вы ввели не существующего студента")
