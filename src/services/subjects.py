from pprint import pprint

from schemas.subjects import (SSubjectsAdd, SSubjectsGroups,
                              SSubjectsTeachers, SSubjectsEdit)
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from utils.unitofwork import UnitOfWork
from core.exceptions import MyException
from sqlalchemy.orm import selectinload
from models.subjects import Subjects
from sqlalchemy import select
from uuid import UUID
import importlib


class SubjectsService:

    @staticmethod
    async def __get_groups(uow: UnitOfWork, groups_uuid: list[UUID]):
        """
        We get groups. Using the GroupsService group service
        """
        module = importlib.import_module("services.groups")
        list_groups = []
        for uuid in groups_uuid:
            groups = await module.GroupsService().get_groups_with_filter_uuid(uow, uuid)
            if not groups:
                raise MyException(status_code=409, message="This group does not exist. "
                                                           "Add group to database")
            else:
                list_groups.append(groups)
        return list_groups

    @staticmethod
    async def __get_teachers(uow: UnitOfWork, teachers_uuid: list[UUID]):
        """
        We get teachers.
        Using TeachersService
        """
        module = importlib.import_module("services.teachers")
        list_teachers = []
        for uuid in teachers_uuid:
            teachers = await module.TeachersService().get_teachers_with_filter_uuid(uow, uuid)
            if not teachers:
                raise MyException(status_code=409, message="This teacher does not exist. "
                                                           "Add teacher to database")
            else:
                list_teachers.append(teachers)
        return list_teachers

    @staticmethod
    def __convert_the_names_of_objects_to_lower_case_and_perform_validation(name: str):
        """
        Convert all strings to
        small register and do it
        validation of these strings
        """
        data_subjects = {}
        for al in name.replace(' ', ''):
            if not al.isalpha():
                raise MyException(status_code=409, message=f"Exception in convert_the_names_of_objects_"
                                                           f"to_lower_case_and_perform_validation."
                                                           f"The data contains other characters.")
        data_subjects['name'] = name.lower()
        return data_subjects

    @classmethod
    async def add_subjects(cls, uow: UnitOfWork, subjects_schema: SSubjectsAdd):
        """
        Adding educational
        item to the database.
        """
        subjects_schema = subjects_schema.model_dump()

        name: str = subjects_schema.get('name')

        name: dict[str, str] = cls.__convert_the_names_of_objects_to_lower_case_and_perform_validation(name)

        async with uow:
            try:
                subjects_model = await uow.subjects.add_one(name)
                await uow.commit()
                return subjects_model
            except IntegrityError as e:
                pprint(e)
                await uow.session.rollback()
                raise MyException(status_code=409, message=f"An exception occurred in add_subjects - Such a subject "
                                                           f"exists")

    @staticmethod
    async def get_subjects_with_filter_uuid(uow: UnitOfWork, uuid: UUID):
        """
        Getting a subject by UUID
        """
        try:
            async with uow:
                subjects = await uow.subjects.find_one({"uuid": uuid})
                return subjects
        except Exception as e:
            pprint(e)
            MyException(status_code=409, message=f"Exception in get_subjects_with_filter_uuid")

    @staticmethod
    async def delete_subjects(uow: UnitOfWork, subjects_uuid: UUID):
        """
        Remove subjects by UUID
        """
        try:
            async with uow:
                await uow.subjects.delete({"uuid": subjects_uuid})
                await uow.commit()
        except Exception as e:
            pprint(e)
            raise MyException(status_code=505, message=f"The exception was in SubjectsService")

    @staticmethod
    async def delete_groups_from_subjects(uow: UnitOfWork, groups_uuid: UUID, subjects_uuid: UUID):
        """
        Delete a group from an academic subject by UUID
        """
        async with uow:
            try:
                stmt = select(Subjects).filter_by(**{"uuid": subjects_uuid}).options(selectinload(Subjects.groups))
                subjects_model = await uow.session.execute(stmt)
                subjects_model = subjects_model.scalars().first()
            except Exception as e:
                pprint(e)
                raise MyException(status_code=409, message="Exception in delete_groups_from_subjects - "
                                                           "You have entered an incorrect subject ID")
            if not subjects_model:
                raise MyException(status_code=409, message=f"Exception in delete_groups_from_subjects. "
                                                           f"There is no such school subject.")
            try:
                groups_model = await uow.groups.find_one({"uuid": groups_uuid})
            except Exception as e:
                pprint(e)
                raise MyException(status_code=409, message="Exception in delete_groups_from_subjects - "
                                                           "You have entered an incorrect group ID")
            if not groups_model:
                raise MyException(status_code=409, message=f"Exception in delete_groups_from_subjects. "
                                                           f"There is no such group.")
            try:
                subjects_model.groups.remove(groups_model)
            except ValueError as e:
                pprint(e)
                raise MyException(status_code=409, message="You are deleting a group whose "
                                                           "there is no subject")
            uow.session.add(subjects_model)
            await uow.commit()

    @staticmethod
    async def delete_teachers_from_subjects(uow: UnitOfWork, teachers_uuid: UUID, subjects_uuid: UUID):
        """
        Removing a teacher from a subject by UUID
        """
        async with uow:
            try:
                stmt = select(Subjects).filter_by(**{"uuid": subjects_uuid}).options(selectinload(Subjects.teachers))
                subjects_model = await uow.session.execute(stmt)
                subjects_model = subjects_model.scalars().first()
            except Exception as e:
                print(e)
                raise MyException(status_code=409, message="Exception in delete_teachers_from_subjects - "
                                                           "You have entered an incorrect subject ID")
            if not subjects_model:
                raise MyException(status_code=409, message=f"Exception in delete_teachers_from_subjects. "
                                                           f"There is no such educational subject.")
            try:
                teachers_model = await uow.teachers.find_one({"uuid": teachers_uuid})
            except Exception as e:
                print(e)
                raise MyException(status_code=409, message="Exception in delete_teachers_from_subjects - "
                                                           "You have entered an incorrect teacher ID")
            if not teachers_model:
                raise MyException(status_code=409, message=f"Exception in delete_teachers_from_subjects. "
                                                           f"There is no such teacher.")
            try:
                subjects_model.teachers.remove(teachers_model)
            except ValueError as e:
                pprint(e)
                raise MyException(status_code=409, message="You are removing the teacher whose "
                                                           "there is no subject")
            uow.session.add(subjects_model)
            await uow.commit()

    @staticmethod
    async def get_all_subjects_without_groups_and_teachers(uow: UnitOfWork):
        """
        Get all educational items
        """
        try:
            async with uow:
                data_subjects = await uow.subjects.find_all()
                return data_subjects
        except Exception as e:
            pprint(e)
            raise MyException(status_code=505, message=f'Исключение в get_all_subjects')

    @classmethod
    async def add_groups_to_subjects(cls, uow: UnitOfWork, groups_uuid: SSubjectsGroups, subjects_uuid: UUID):
        """
        Adding groups to a subject by UUID
        """
        groups_uuid = groups_uuid.model_dump()
        groups_uuid = groups_uuid.get("groups")
        if not groups_uuid:
            raise MyException(status_code=409, message=f"You haven't added groups")

        groups_model_list = await cls.__get_groups(uow, groups_uuid)

        stm = select(Subjects).filter_by(**{"uuid": subjects_uuid}).options(selectinload(Subjects.groups))
        subjects_model = await uow.service_session.execute(stm)
        subjects_model = subjects_model.scalars().first()

        if not subjects_model:
            raise MyException(status_code=409, message=f"Exception in add_groups_by_subjects. "
                                                       f"There is no such educational subject.")

        try:
            subjects_model.groups.extend(groups_model_list)
        except InvalidRequestError as e:
            pprint(e)
            raise MyException(status_code=409, message="Exception in add_groups_by_subjects. "
                                                       "You add a group that exists for an item")
        uow.service_session.add(subjects_model)
        await uow.service_session.commit()
        await uow.service_session.close()

    @classmethod
    async def add_teachers_to_subjects(cls, uow: UnitOfWork, teachers_uuid: SSubjectsTeachers, subjects_uuid: UUID):
        """
        Adding teachers to a subject
        """
        teachers_uuid = teachers_uuid.model_dump()
        teachers_uuid = teachers_uuid.get("teachers")
        if not teachers_uuid:
            raise MyException(status_code=409, message=f"You haven't added a teacher")

        teachers_model_list = await cls.__get_teachers(uow, teachers_uuid)

        stm = select(Subjects).filter_by(**{"uuid": subjects_uuid}).options(selectinload(Subjects.teachers))
        subjects_model = await uow.service_session.execute(stm)
        subjects_model = subjects_model.scalars().first()

        if not subjects_model:
            raise MyException(status_code=409, message=f"Exception in add_teachers_to_subjects."
                                                       f"There is no such educational subject.")

        try:
            subjects_model.teachers.extend(teachers_model_list)
        except InvalidRequestError as e:
            pprint(e)
            raise MyException(status_code=409, message="Exception in add_teachers_to_subjects. "
                                                       "You are adding a teacher who does not exist for the subject")
        uow.service_session.add(subjects_model)
        await uow.service_session.commit()

    @classmethod
    async def edit_only_subjects(cls, uow: UnitOfWork, subjects_schema: SSubjectsEdit, subjects_uuid: UUID):
        """
        We update a subject without its teachers and groups
        """
        subjects_schema = subjects_schema.model_dump()
        subjects_data = cls.__convert_the_names_of_objects_to_lower_case_and_perform_validation(
            subjects_schema.get('name'))

        try:
            async with uow:
                await uow.subjects.edit_one(subjects_uuid, subjects_data)
                await uow.commit()
        except Exception as e:
            pprint(e)
            raise MyException(status_code=409, message="Exception in edit_only_subjects")

    @staticmethod
    async def get_all_subjects_with_groups(uow: UnitOfWork):
        """
        Get all teachers with their groups
        """
        try:
            stmt = select(Subjects).options(selectinload(Subjects.groups))
            res = await uow.service_session.execute(stmt)
            res = res.scalars().all()
            await uow.service_session.close()
            return res
        except Exception as e:
            pprint(e)
            raise MyException(status_code=500, message=f"Exception in get_all_subjects_with_groups")

    @staticmethod
    async def get_all_subjects_with_teachers(uow: UnitOfWork):
        """
        Get all teachers with their teachers
        """
        try:
            stmt = select(Subjects).options(selectinload(Subjects.teachers))
            res = await uow.service_session.execute(stmt)
            res = res.scalars().all()
            await uow.service_session.close()
            return res
        except Exception as e:
            pprint(e)
            raise MyException(status_code=500, message=f"Exception in get_all_subjects_with_teachers")
