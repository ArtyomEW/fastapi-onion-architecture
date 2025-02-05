from models.groups import Groups
from schemas.teachers import (STeacherAdd, STeachersEdit,
                              STeachersSubjects, STeachersGroups)
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from core.security import get_password_hash
from utils.unitofwork import UnitOfWork
from core.exceptions import MyException
from sqlalchemy.orm import selectinload
from models.teachers import Teachers
from sqlalchemy import select
from pprint import pprint
from uuid import UUID
import importlib


class TeachersService:

    @staticmethod
    async def __get_subjects(uow: UnitOfWork, subjects_uuid: list[UUID]) -> list:
        """
        We receive educational items. Using the SubjectsService group service
        """
        module = importlib.import_module("services.subjects")
        list_subjects = []
        for uuid in subjects_uuid:
            subjects = await module.SubjectsService().get_subjects_with_filter_uuid(uow, uuid)
            if not subjects:
                raise MyException(status_code=409, message="The exception in TeachersService is get_subjects. "
                                                           "This item does not exist."
                                                           "Add item to database")
            else:
                list_subjects.append(subjects)
        return list_subjects

    @staticmethod
    async def __get_groups(uow: UnitOfWork, groups_uuid: list[UUID]) -> list:
        """
        We get groups. Using the GroupsService group service
        """
        module = importlib.import_module("services.groups")
        list_groups = []
        for uuid in groups_uuid:
            groups = await module.GroupsService().get_groups_with_filter_uuid(uow, uuid)
            if not groups:
                raise MyException(status_code=409, message="Exception in TeachersService. "
                                                           "This group does not exist."
                                                           "Add group to database")
            else:
                list_groups.append(groups)
        return list_groups

    @staticmethod
    def __convert_lines_to_small_letters_in_teachers_service(teachers_schema: dict[str, str]) -> dict:
        """
        Convert all strings to
        small register and do it
        validation of these strings
        """
        data_teachers = {}
        for key, value in teachers_schema.items():
            if value and (key != "login") and (key != 'hashed_password') and (key != 'is_role'):
                for al in value.replace(' ', ''):
                    if not al.isalpha():
                        raise MyException(status_code=409, message=f"Exception in "
                                                                   f"__convert_lines_to_small_"
                                                                   f"letters_in_teachers_service."
                                                                   f" The data contains other characters.")
                data_teachers[key] = value.lower()
            else:
                if key == 'hashed_password':
                    data_teachers[key] = get_password_hash(value)
                else:
                    data_teachers[key] = value
        return data_teachers

    @classmethod
    async def add_teachers(cls, uow: UnitOfWork, teachers_schema: STeacherAdd):
        """
        Adding a teacher to
        database without subjects and groups
        """

        teachers_schema = teachers_schema.model_dump()
        teachers = cls.__convert_lines_to_small_letters_in_teachers_service(teachers_schema)

        async with uow:
            try:
                await uow.teachers.add_one(teachers)
                await uow.commit()
                return teachers
            except IntegrityError as e:
                await uow.session.rollback()
                pprint(e)
                raise MyException(status_code=409, message=f"An exception occurred in add_subjects")

    @staticmethod
    async def get_teachers_with_filter_uuid(uow: UnitOfWork, teacher_uuid: UUID):
        """
        Finding a teacher by UUID
        """
        try:
            async with uow:
                teachers = await uow.teachers.find_one({'uuid': teacher_uuid})
                return teachers
        except Exception as e:
            pprint(e)
            raise MyException(status_code=409, message=f"Exception in get_teachers_with_filter_uuid. "
                                                       f"You may have entered a non-existent teacher")

    @staticmethod
    async def delete_teacher(uow: UnitOfWork, teacher_uuid: UUID):
        """
        Removing a teacher by uuid
        """
        try:
            async with uow:
                await uow.teachers.delete({'uuid': teacher_uuid})
                await uow.commit()
        except Exception as e:
            pprint(e)
            raise MyException(status_code=409, message=f'Exception in delete_teacher')

    @staticmethod
    async def get_all_teachers(uow: UnitOfWork):
        """
        Get all teachers without academic subjects
        """
        try:
            async with uow:
                data_teachers = await uow.teachers.find_all()
                return data_teachers
        except Exception as e:
            pprint(e)
            raise MyException(status_code=505, message=f"Exception in get_all_teachers")

    @staticmethod
    async def get_all_teachers_with_groups(uow: UnitOfWork):
        """
        Get all teachers with their groups
        """
        try:
            stmt = select(Teachers).options(selectinload(Teachers.groups))
            res = await uow.service_session.execute(stmt)
            res = res.scalars().all()
            await uow.service_session.close()
            return res
        except Exception as e:
            pprint(e)
            raise MyException(status_code=505, message="Exception in get_all_teachers_with_groups")

    @staticmethod
    async def get_all_teachers_with_subjects(uow: UnitOfWork):
        """
        Get all teachers with their academic subjects
        """
        try:
            stmt = select(Teachers).options(selectinload(Teachers.subjects))
            res = await uow.service_session.execute(stmt)
            res = res.scalars().all()
            await uow.service_session.close()
            return res
        except Exception as e:
            pprint(e)
            raise MyException(status_code=505, message="Exception in get_all_teachers_with_groups")

    @classmethod
    async def edit_only_teachers(cls, uow: UnitOfWork, teacher_schema: STeachersEdit, teachers_uuid: UUID):
        """
        Update the teacher without affecting his subjects and groups
        """
        teacher_schema = teacher_schema.model_dump()
        teacher_schema = cls.__convert_lines_to_small_letters_in_teachers_service(teacher_schema)

        try:

            async with uow:
                await uow.teachers.edit_one(teachers_uuid, teacher_schema)
                await uow.commit()

        except Exception as e:
            pprint(e)
            raise MyException(status_code=409, message=f"Exception in edit_only_teachers")

    @classmethod
    async def add_subjects_by_teachers(cls, uow: UnitOfWork,
                                       subjects_uuid: STeachersSubjects, teachers_uuid: UUID):
        """
        Adding subjects to teachers
        """
        subjects_uuid = subjects_uuid.model_dump()
        subjects_uuid = subjects_uuid.get('subjects')

        if not subjects_uuid:
            raise MyException(status_code=409, message=f"Exception in add_subjects_by_teachers. "
                                                       f"You haven't added a subject")

        stmt = select(Teachers).filter_by(**{"uuid": teachers_uuid}).options(selectinload(Teachers.subjects))
        teachers_model = await uow.service_session.execute(stmt)
        teachers_model = teachers_model.scalars().first()

        if not teachers_model:
            raise MyException(status_code=409, message=f"Exception in add_subjects_by_teachers. "
                                                       f"Teacher not found.")

        list_subjects = await cls.__get_subjects(uow, subjects_uuid)

        teachers_model.subjects.extend(list_subjects)

        uow.service_session.add(teachers_model)
        await uow.service_session.commit()
        await uow.service_session.close()

    @classmethod
    async def add_groups_by_teachers(cls, uow: UnitOfWork, groups_uuid: STeachersGroups, teachers_uuid: UUID):
        """
        Adding groups to the teacher
        """

        groups_uuid = groups_uuid.model_dump()
        groups_uuid = groups_uuid.get('groups')
        if not groups_uuid:
            raise MyException(status_code=409, message=f"Exception in add_groups_by_teachers. "
                                                       f"You haven't added a group.")

        list_groups = await cls.__get_groups(uow, groups_uuid)

        stm = select(Teachers).filter_by(**{"uuid": teachers_uuid}).options(selectinload(Teachers.groups))
        teachers_model = await uow.service_session.execute(stm)
        teachers_model = teachers_model.scalars().first()

        if not teachers_model:
            raise MyException(status_code=409, message=f"Exception in add_groups_by_teachers. "
                                                       f"There is no such teacher.")
        try:
            teachers_model.groups.extend(list_groups)
        except InvalidRequestError as e:
            pprint(e)
            raise MyException(status_code=409, message="Exception in add_groups_by_teachers. "
                                                       "You are adding a group that exists with the teacher")
        uow.service_session.add(teachers_model)
        await uow.service_session.commit()

    @classmethod
    async def delete_subjects_from_teachers(cls, uow: UnitOfWork, subjects_uuid: UUID, teachers_uuid: UUID):
        """
        Removing a subject from a teacher
        """
        async with uow:
            try:
                stmt = select(Teachers).filter_by(**{"uuid": teachers_uuid}).options(selectinload(Teachers.subjects))
                teachers_model = await uow.session.execute(stmt)
                teachers_model = teachers_model.scalars().first()
            except Exception as e:
                pprint(e)
                raise MyException(status_code=409, message="Exception in delete_subjects_from_teachers - "
                                                           "You have entered an incorrect teacher ID")
            if not teachers_model:
                raise MyException(status_code=409, message=f"Exception in delete_subjects_from_teachers. "
                                                           f"There is no such teacher.")
            try:
                subjects_model = await uow.subjects.find_one({"uuid": subjects_uuid})
            except Exception as e:
                pprint(e)
                raise MyException(status_code=409, message="Exception in delete_subjects_from_teachers - "
                                                           "You have entered an incorrect subject ID")
            if not subjects_model:
                raise MyException(status_code=409, message=f"Exception in delete_subjects_from_teachers. "
                                                           f"There is no such item.")
            try:
                teachers_model.subjects.remove(subjects_model)
            except ValueError as e:
                pprint(e)
                raise MyException(status_code=409, message="You are deleting a school subject that "
                                                           "there is no teacher")
            uow.session.add(teachers_model)
            await uow.commit()

    @classmethod
    async def delete_groups_from_teachers(cls, uow: UnitOfWork, groups_uuid: UUID, teachers_uuid: UUID):
        """
        Delete a teacher's group by UUID
        """
        async with uow:
            try:
                stmt = select(Teachers).filter_by(**{"uuid": teachers_uuid}).options(selectinload(Teachers.groups))
                teachers_model = await uow.session.execute(stmt)
                teachers_model = teachers_model.scalars().first()
            except Exception as e:
                pprint(e)
                raise MyException(status_code=409, message="Exception in delete_groups_from_teachers - "
                                                           "You have entered an incorrect teacher ID")
            if not teachers_model:
                raise MyException(status_code=409, message=f"Exception in delete_groups_from_teachers. "
                                                           f"There is no such teacher.")
            try:
                groups_model = await uow.groups.find_one({"uuid": groups_uuid})
            except Exception as e:
                pprint(e)
                raise MyException(status_code=409, message="Exception in delete_groups_from_teachers - "
                                                           "You have entered an incorrect item group ID")
            if not groups_model:
                raise MyException(status_code=409, message=f"Exception in delete_groups_from_teachers. "
                                                           f"There is no such group.")
            try:
                teachers_model.groups.remove(groups_model)
            except ValueError:
                raise MyException(status_code=409, message="You are deleting a group whose "
                                                           "there is no teacher")
            try:
                uow.session.add(teachers_model)
            except Exception as e:
                pprint(e)
                raise MyException(status_code=500, message=f"Exception in delete_groups_from_teachers")
            await uow.commit()

    @staticmethod
    async def get_the_teacher_and_his_groups(uow: UnitOfWork, teacher_uuid: UUID):
        """
        get the teacher and his groups
        """
        stmt = (select(Teachers).filter_by(**{"uuid": teacher_uuid}).
                options(selectinload(Teachers.groups).selectinload(Groups.students)))

