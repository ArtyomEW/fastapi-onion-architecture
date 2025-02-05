from schemas.students import (SStudentsAdd, SStudentsGroups, SStudentsEdit)
from core.security import get_password_hash
from sqlalchemy.exc import IntegrityError
from utils.unitofwork import UnitOfWork
from core.exceptions import MyException
from sqlalchemy.orm import selectinload
from models.teachers import Teachers
from models.students import Students
from models.groups import Groups
from sqlalchemy import select
from uuid import UUID
import importlib


class StudentsService:
    @staticmethod
    async def __get_groups(uow: UnitOfWork, groups_uuid: UUID):
        """
        We get a group. Using the GroupsService group service
        """
        module = importlib.import_module("services.groups")
        groups = await module.GroupsService().get_groups_with_filter_uuid(uow, groups_uuid)
        if not groups:
            raise MyException(status_code=409, message="Exception in StudentsService. "
                                                       "This group does not exist."
                                                       "Add group to database")
        return groups

    @staticmethod
    def __convert_lines_to_small_letters(students_schema: dict[str, str]) -> dict:
        """
        Convert all strings to
        small register and do it
        validation of these strings
        """
        data_students = {}
        for key, value in students_schema.items():
            if value and (key != "login" and key != 'hashed_password'):
                for al in value:
                    if not al.isalpha():
                        raise MyException(status_code=409, message=f"Exception in __convert_lines_to_small_letters. "
                                                                   f"The data contains other characters.")
                data_students[key] = value.lower()
            else:
                if key == 'hashed_password':
                    data_students[key] = get_password_hash(value)
                else:
                    data_students[key] = value
        return data_students

    @classmethod
    async def add_student(cls, uow: UnitOfWork, student_schema: SStudentsAdd):
        """
        Adding a student without a group
        """
        student_schema: dict = student_schema.model_dump()
        student_schema = cls.__convert_lines_to_small_letters(student_schema)

        async with uow:
            student_model = await uow.students.add_one(student_schema)
            try:
                await uow.commit()
                return student_model
            except IntegrityError as e:
                await uow.session.rollback()
                raise MyException(status_code=505, message=f"An exception occurred in add_student. "
                                                           f"This login already exists")

    @classmethod
    async def add_groups_to_students(cls, uow: UnitOfWork, groups_schema: SStudentsGroups, students_uuid: UUID):
        """
        Adding a group to a student
        """
        groups_schema = groups_schema.model_dump()
        group_uuid = groups_schema.get("group")

        if not group_uuid:
            raise MyException(status_code=409, message=f"Exception in add_groups_to_students. "
                                                       f"You haven't added a group")

        stmt = select(Students).filter_by(**{"uuid": students_uuid}).options(selectinload(Students.groups))
        students_model = await uow.service_session.execute(stmt)
        students_model = students_model.scalars().first()

        if not students_model:
            raise MyException(status_code=409, message=f"Exception in add_groups_to_students. "
                                                       f"Student not found.")

        group_model = await cls.__get_groups(uow, group_uuid)

        students_model.groups = group_model

        uow.service_session.add(students_model)
        await uow.service_session.commit()
        await uow.service_session.close()

    @staticmethod
    async def get_students_subjects_and_teachers(uow: UnitOfWork):
        """
        We get the student and his groups,
        his teachers and his subjects
        """
        try:
            stmt = (select(Students)
                    .options(selectinload(Students.groups),
                             selectinload(Students.groups).selectinload(Groups.subjects),
                             selectinload(Students.groups).selectinload(Groups.teachers).selectinload(
                                 Teachers.subjects), ))
            res = await uow.service_session.execute(stmt)
            res = res.scalars().all()
            await uow.service_session.close()
            return res
        except Exception as e:
            print(e)
            raise MyException(status_code=505, message=f"Exception in get_subjects_and_teachers")

    @staticmethod
    async def get_only_students(uow: UnitOfWork):
        """
        Get all students but without their groups
        """
        try:
            async with uow:
                students = await uow.students.find_all()
                return students
        except Exception as e:
            print(e)
            raise MyException(status_code=500, message="Exception in get_only_students")

    @staticmethod
    async def get_students_with_groups(uow: UnitOfWork):
        """
        Get students and their groups
        """
        try:
            stmt = select(Students).options(selectinload(Students.groups))
            students_model = await uow.service_session.execute(stmt)
            await uow.service_session.close()
            return students_model
        except Exception as e:
            print(e)
            raise MyException(status_code=500, message="Exception in get_students_with_groups")

    @staticmethod
    async def get_students_with_filter_uuid(uow: UnitOfWork, students_uuid: UUID):
        """
        Get student by UUID
        """
        try:
            async with uow:
                students = await uow.students.find_one({'uuid': students_uuid})
                return students
        except Exception as e:
            raise MyException(status_code=409, message=f"Exception in get_students_with_filter_uuid. "
                                                       f"You may have entered a non-existent student")

    @staticmethod
    async def delete_students(uow: UnitOfWork, students_uuid: UUID):
        """
        Removing a student by UUID
        """
        try:
            async with uow:
                await uow.students.delete({"uuid": students_uuid})
                await uow.commit()
        except Exception as e:
            print(e)
            raise MyException(status_code=409, message=f"Exception in delete_students")

    @staticmethod
    async def delete_groups_from_students(uow: UnitOfWork, students_uuid: UUID, groups_uuid: UUID):
        """
        Removing a group from a student by UUID
        """
        async with uow:
            try:
                stmt = select(Students).filter_by(**{"uuid": students_uuid}).options(selectinload(Students.groups))
                students_model = await uow.session.execute(stmt)
                students_model = students_model.scalars().first()
            except Exception as e:
                print(e)
                raise MyException(status_code=409, message="Exception in delete_groups_from_students - "
                                                           "You entered the wrong student ID")
            if not students_model:
                raise MyException(status_code=409, message=f"Exception in delete_groups_from_students. "
                                                           f"There is no such student.")
            try:
                groups_model = await uow.groups.find_one({"uuid": groups_uuid})
            except Exception as e:
                print(e)
                raise MyException(status_code=409, message="Exception in delete_groups_from_students - "
                                                           "You have entered an incorrect group ID")
            if not groups_model:
                raise MyException(status_code=409, message=f"Exception in delete_groups_from_students. "
                                                           f"There is no such group.")
            try:
                students_model.groups = None
            except ValueError as e:
                print(e)
                raise MyException(status_code=409, message="You are deleting a group whose "
                                                           "the student does not have")
            uow.session.add(students_model)
            await uow.commit()

    @classmethod
    async def update_students_by_UUID(cls, uow: UnitOfWork, students_schema: SStudentsEdit, students_uuid: UUID):
        """
        We update the student by UUID, but we cannot touch his group
        """
        students_schema = students_schema.model_dump()
        data_students = cls.__convert_lines_to_small_letters(students_schema)
        async with uow:
            try:
                await uow.students.edit_one(students_uuid, data_students)
                await uow.commit()
            except Exception as e:
                await uow.rollback()
                print(e)
                raise MyException(status_code=409, message="Exception in update_students_by_UUID")
