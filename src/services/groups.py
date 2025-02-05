from schemas.groups import (SGroupsAdd, SGroupsSubjects,
                            SGroupsStudents, SGroupsTeachers, SGroupsEdit)
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import selectinload
from utils.unitofwork import UnitOfWork
from core.exceptions import MyException
from models.groups import Groups
from sqlalchemy import select
from uuid import UUID
import importlib


class GroupsService:

    @staticmethod
    async def __get_students(uow: UnitOfWork, students_uuid: list[UUID]) -> list:
        """
        We get students with
        using the StudentService service
        """
        module = importlib.import_module("services.students")
        list_students = []
        for uuid in students_uuid:
            student_model = await module.StudentsService().get_students_with_filter_uuid(uow, uuid)
            if not student_model:
                raise MyException(status_code=409, message="This student does not exist."
                                                           "Add student to database")
            else:
                list_students.append(student_model)
        return list_students

    @staticmethod
    async def __get_subjects(uow: UnitOfWork, subjects_uuid: list[UUID]) -> list:
        """
        We receive items from
        using the SubjectsService service
        """
        module = importlib.import_module("services.subjects")
        list_subjects = []
        for subject in subjects_uuid:
            subjects_model = await module.SubjectsService().get_subjects_with_filter_uuid(uow, subject)
            if not subjects_model:
                raise MyException(status_code=409, message="This item does not exist."
                                                           "Add item to database")
            else:
                list_subjects.append(subjects_model)
        return list_subjects

    @staticmethod
    async def __get_teachers(uow: UnitOfWork, teachers_uuid: list[UUID]) -> list:
        """
        We get teachers with
        using the TeachersService service
        """
        module = importlib.import_module("services.teachers")
        list_teachers = []
        for teacher in teachers_uuid:
            teacher_model = await module.TeachersService().get_teachers_with_filter_uuid(uow, teacher)
            if not teacher_model:
                raise MyException(status_code=409, message="This teacher doesn't exist."
                                                           "Add teacher to database")
            else:
                list_teachers.append(teacher_model)
        return list_teachers

    @staticmethod
    def __are_there_any_letters_in_the_group_number_etc(number_group: str):
        """
        We check if there is in the room
        groups of letters or other symbols
        """
        if not number_group:
            raise MyException(status_code=409, message="Напишите группу")
        for v in number_group.replace(' ', ''):
            if not v.isdigit():
                raise MyException(status_code=409, message="The group number must "
                                                           "consist only of numbers")

    @classmethod
    async def add_groups(cls, uow: UnitOfWork, groups_schema: SGroupsAdd):
        """
        Add a group without students, subjects and teachers.
        """

        groups_schema = groups_schema.model_dump()

        number_group = groups_schema.get('number_group')
        cls.__are_there_any_letters_in_the_group_number_etc(number_group)

        async with uow:
            group_model = await uow.groups.add_one(groups_schema)
            try:
                await uow.commit()
                return group_model
            except IntegrityError:
                await uow.session.rollback()
                raise MyException(status_code=409, message="An exception occurred in add_groups."
                                                           "Such a group already exists")

    @classmethod
    async def add_subjects_to_groups(cls, uow: UnitOfWork, subjects_list_uuid: SGroupsSubjects, groups_uuid: UUID):
        """
        Adding educational subjects to the group
        """
        subjects_list_uuid = subjects_list_uuid.model_dump()
        subjects_list_uuid = subjects_list_uuid.get("subjects")
        if not subjects_list_uuid:
            raise MyException(status_code=409, message=f"You haven't added school items")

        subjects_model_list = await cls.__get_subjects(uow, subjects_list_uuid)

        stm = select(Groups).filter_by(**{"uuid": groups_uuid}).options(selectinload(Groups.subjects))
        groups_model = await uow.service_session.execute(stm)
        groups_model = groups_model.scalars().first()

        if not groups_model:
            raise MyException(status_code=409, message=f"Exception in add_subjects_to_groups. "
                                                       f"There is no such group.")

        try:
            groups_model.subjects.extend(subjects_model_list)
        except InvalidRequestError as e:
            print(e)
            raise MyException(status_code=409, message="Exception in add_subjects_to_groups. "
                                                       "You add educational subjects that the group has")
        uow.service_session.add(groups_model)
        await uow.service_session.commit()
        await uow.service_session.close()

    @classmethod
    async def add_students_to_groups(cls, uow: UnitOfWork, students_list_uuid: SGroupsStudents, groups_uuid: UUID):
        """
        Adding students to the group
        """
        students_list_uuid = students_list_uuid.model_dump()
        students_list_uuid = students_list_uuid.get("students")
        if not students_list_uuid:
            raise MyException(status_code=409, message=f"You haven't added students")

        students_model_list = await cls.__get_students(uow, students_list_uuid)

        stm = select(Groups).filter_by(**{"uuid": groups_uuid}).options(selectinload(Groups.students))
        groups_model = await uow.service_session.execute(stm)
        groups_model = groups_model.scalars().first()

        if not groups_model:
            raise MyException(status_code=409, message=f"Exception in add_students_to_groups. "
                                                       f"There is no such group.")

        try:
            groups_model.students.extend(students_model_list)
        except InvalidRequestError as e:
            print(e)
            raise MyException(status_code=409, message="Exception in add_students_to_groups. "
                                                       "You are adding students who exist in the group")
        uow.service_session.add(groups_model)
        await uow.service_session.commit()
        await uow.service_session.close()

    @classmethod
    async def add_teachers_to_groups(cls, uow: UnitOfWork, teachers_list_uuid: SGroupsTeachers, groups_uuid: UUID):
        """
        Adding teachers to a group by UUID
        """
        teachers_list_uuid = teachers_list_uuid.model_dump()
        teachers_list_uuid = teachers_list_uuid.get("teachers")
        if not teachers_list_uuid:
            raise MyException(status_code=409, message=f"Adding teachers to the group")

        teachers_model_list = await cls.__get_teachers(uow, teachers_list_uuid)

        stm = select(Groups).filter_by(**{"uuid": groups_uuid}).options(selectinload(Groups.teachers))
        groups_model = await uow.service_session.execute(stm)
        groups_model = groups_model.scalars().first()

        if not groups_model:
            raise MyException(status_code=409, message=f"Exception in add_students_to_groups. "
                                                       f"There is no such group.")

        try:
            groups_model.teachers.extend(teachers_model_list)
        except InvalidRequestError as e:
            print(e)
            raise MyException(status_code=409, message="Exception in add_teachers_to_groups. "
                                                       "You add teachers who exist in the group")
        uow.service_session.add(groups_model)
        await uow.service_session.commit()
        await uow.service_session.close()

    @classmethod
    async def updating_a_group_without_affecting_its_dependent_entities(cls, uow: UnitOfWork,
                                                                        groups_schema: SGroupsEdit,
                                                                        groups_uuid: UUID):
        """
        Updating a group without affecting its dependent entities
        """
        groups_schema = groups_schema.model_dump()
        cls.__are_there_any_letters_in_the_group_number_etc(groups_schema.get('number_group'))

        try:
            async with uow:
                await uow.groups.edit_one(groups_uuid, groups_schema)
                await uow.commit()
        except Exception as e:
            print(e)
            raise MyException(status_code=500, message="Exception in updating_a_group_without_"
                                                       "affecting_its_dependent_entities")

    @classmethod
    async def get_groups_with_filter_uuid(cls, uow: UnitOfWork, groups_uuid: UUID):
        """
        Get group by UUID
        """
        async with uow:
            try:
                group_model = await uow.groups.find_one({"uuid": groups_uuid})
                if not group_model:
                    raise MyException(status_code=409, message="Exception in get_groups_with_filter_uuid."
                                                               "There is no such group")
                return group_model
            except Exception as e:
                raise MyException(status_code=505, message=f"Exception in get_groups_with_filter - {e}")

    @classmethod
    async def getting_a_group_by_group_number(cls, uow: UnitOfWork, number_group: str):
        """
        Get group by group number
        """
        cls.__are_there_any_letters_in_the_group_number_etc(number_group)

        async with uow:
            try:
                groups = await uow.groups.find_one({"number_group": number_group})
                return groups
            except Exception as e:
                raise MyException(status_code=505, message=f"Exception in get_groups_with_filter - {e}")

    @staticmethod
    async def get_groups_without_students_and_teachers_and_subjects(uow: UnitOfWork):
        """
        Get all groups without students, without teachers and without subjects
        """
        try:
            async with uow:
                groups = await uow.groups.find_all()
                return groups
        except Exception as e:
            raise MyException(status_code=505, message=f"Exception in get_only_groups - {e}")

    @staticmethod
    async def get_groups_with_subjects(uow: UnitOfWork):
        """
        Get all groups with academic subjects
        """
        try:
            stmt = select(Groups).options(selectinload(Groups.subjects))
            res = await uow.service_session.execute(stmt)
            res = res.scalars().all()
            await uow.service_session.close()
            return res
        except Exception as e:
            print(e)
            raise MyException(status_code=505, message="Exception in get_groups_with_subjects")

    @staticmethod
    async def get_groups_with_students(uow: UnitOfWork):
        """
        Get all groups with students
        """
        try:
            stmt = select(Groups).options(selectinload(Groups.students))
            res = await uow.service_session.execute(stmt)
            res = res.scalars().all()
            await uow.service_session.close()
            return res
        except Exception as e:
            print(e)
            raise MyException(status_code=505, message="Exception in get_groups_with_students")

    @staticmethod
    async def get_groups_with_teachers(uow: UnitOfWork):
        """
        Get all groups with teachers
        """
        try:
            stmt = select(Groups).options(selectinload(Groups.teachers))
            res = await uow.service_session.execute(stmt)
            res = res.scalars().all()
            await uow.service_session.close()
            return res
        except Exception as e:
            print(e)
            raise MyException(status_code=505, message="Exception in get_groups_with_teachers")

    @staticmethod
    async def get_one_group_with_filter_uuid(uow: UnitOfWork, uuid: str):
        """
        Getting the group by UUID
        """
        try:
            async with uow:
                groups = await uow.groups.find_one({'uuid': uuid})
                return groups
        except Exception as e:
            print(e)
            raise MyException(status_code=409, message=f"Exception in get_groups_with_filter_uuid."
                                                       f"You have entered a group that does not exist")

    @staticmethod
    async def delete_groups_by_UUID(uow: UnitOfWork, groups_uuid: UUID):
        """
        Remove groups by UUID
        """
        try:
            async with uow:
                await uow.groups.delete({'uuid': groups_uuid})
                await uow.commit()
        except Exception as e:
            print(e)
            raise MyException(status_code=409, message=f"Exception in delete_groups")

    @staticmethod
    async def service_delete_subjects_from_groups(uow: UnitOfWork, subjects_uuid: UUID, groups_uuid: UUID):
        """
        Deleting educational items from a group by UUID
        """
        async with uow:
            try:
                stmt = select(Groups).filter_by(**{"uuid": groups_uuid}).options(selectinload(Groups.subjects))
                groups_model = await uow.session.execute(stmt)
                groups_model = groups_model.scalars().first()
            except Exception as e:
                print(e)
                raise MyException(status_code=409, message="Exception in service_delete_subjects_from_groups - "
                                                           "You entered the wrong group ID")
            if not groups_model:
                raise MyException(status_code=409, message=f"Exception in service_delete_subjects_from_groups."
                                                           f"There is no such group.")
            try:
                subjects_model = await uow.subjects.find_one({"uuid": subjects_uuid})
            except Exception as e:
                print(e)
                raise MyException(status_code=409, message="Exception in service_delete_subjects_from_groups - "
                                                           "You have entered an incorrect subject ID")
            if not subjects_model:
                raise MyException(status_code=409, message=f"Exception in service_delete_subjects_from_groups. "
                                                           f"There is no such educational subject.")
            try:
                groups_model.subjects.remove(subjects_model)
            except ValueError as e:
                print(e)
                raise MyException(status_code=409, message="You are deleting a school subject that "
                                                           "there is no teacher")
            uow.session.add(groups_model)
            await uow.commit()

    @staticmethod
    async def service_delete_teachers_from_groups(uow: UnitOfWork, teachers_uuid: UUID, groups_uuid: UUID):
        """
        Removing teachers from a group by UUID
        """
        async with uow:
            try:
                stmt = select(Groups).filter_by(**{"uuid": groups_uuid}).options(selectinload(Groups.teachers))
                groups_model = await uow.session.execute(stmt)
                groups_model = groups_model.scalars().first()
            except Exception as e:
                print(e)
                raise MyException(status_code=409, message="Exception in service_delete_subjects_from_groups - "
                                                           "You entered the wrong group ID")
            if not groups_model:
                raise MyException(status_code=409, message=f"Exception in service_delete_subjects_from_groups. "
                                                           f"There is no such group.")
            try:
                teachers_model = await uow.teachers.find_one({"uuid": teachers_uuid})
            except Exception as e:
                print(e)
                raise MyException(status_code=409, message="Exception in service_delete_teachers_from_groups - "
                                                           "You have entered an incorrect teacher ID")
            if not teachers_model:
                raise MyException(status_code=409, message=f"Exception in service_delete_teachers_from_groups. "
                                                           f"There is no such teacher.")
            try:
                groups_model.teachers.remove(teachers_model)
            except ValueError as e:
                print(e)
                raise MyException(status_code=409, message="You are removing the teacher whose "
                                                           "the group doesn't have")
            uow.session.add(groups_model)
            await uow.commit()

    @staticmethod
    async def service_delete_students_from_groups(uow: UnitOfWork, students_uuid: UUID, groups_uuid: UUID):
        """
        Removing students from a group by UUID
        """
        async with uow:
            try:
                stmt = select(Groups).filter_by(**{"uuid": groups_uuid}).options(selectinload(Groups.students))
                groups_model = await uow.session.execute(stmt)
                groups_model = groups_model.scalars().first()
            except Exception as e:
                print(e)
                raise MyException(status_code=409, message="Exception in service_delete_students_from_groups - "
                                                           "You have entered an incorrect group ID")
            if not groups_model:
                raise MyException(status_code=409, message=f"Exception in service_delete_students_from_groups. "
                                                           f"There is no such group.")
            try:
                students_model = await uow.teachers.find_one({"uuid": students_uuid})
            except Exception as e:
                print(e)
                raise MyException(status_code=409, message="Exception in service_delete_students_from_groups. "
                                                           f"There is no such group.")
            if not students_model:
                raise MyException(status_code=409, message=f"Exception in service_delete_students_from_groups. "
                                                           f"There is no such student.")
            try:
                groups_model.students.remove(students_model)
            except ValueError as e:
                print(e)
                raise MyException(status_code=409, message="You are deleting a student whose "
                                                           "the group doesn't have one")
            uow.session.add(groups_model)
            await uow.commit()
