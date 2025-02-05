from schemas.groups import (SGroupsAdd, SGroupsSubjects, SGroupsStudents,
                            SGroupsTeachers, SGroupsEdit)
from fastapi import APIRouter, status, Depends
from api.dependencies import UOWDep, limiter
from services.groups import GroupsService
from starlette.requests import Request
from typing import Annotated
from uuid import UUID

router = APIRouter(prefix='/admin/groups',
                   tags=['AdminGroups'])


@router.post('/', description="Add groups",
             status_code=status.HTTP_201_CREATED, )
@limiter.limit("5/minute")
async def add_groups(request: Request, uow: UOWDep, groups_schema: Annotated[SGroupsAdd, Depends()]):
    """
    Add a group without students, subjects and teachers.
    """
    group_model = await GroupsService().add_groups(uow, groups_schema)
    return group_model


@router.post('/subjects/{groups_uuid}',
             description="Add subjects to groups",
             status_code=status.HTTP_201_CREATED, )
async def add_subjects_to_groups(uow: UOWDep, subjects_list_uuid: SGroupsSubjects, groups_uuid: UUID):
    """
    Adding educational subjects to the group
    """
    group_model = await GroupsService().add_subjects_to_groups(uow, subjects_list_uuid, groups_uuid)
    return group_model


@router.post('/students/{groups_uuid}',
             description="Add students to groups",
             status_code=status.HTTP_201_CREATED, )
async def add_students_to_groups(uow: UOWDep, students_list_uuid: SGroupsStudents, groups_uuid: UUID):
    """
    Adding students to the group
    """
    group_model = await GroupsService().add_students_to_groups(uow, students_list_uuid, groups_uuid)
    return group_model


@router.post('/teachers/{groups_uuid}',
             description="Add teachers to groups",
             status_code=status.HTTP_201_CREATED, )
async def add_teachers_to_groups(uow: UOWDep, teachers_list_uuid: SGroupsTeachers, groups_uuid: UUID):
    """
    Adding teachers to a group by UUID
    """
    group_model = await GroupsService().add_teachers_to_groups(uow, teachers_list_uuid, groups_uuid)
    return group_model


@router.put('/{groups_uuid}',
            description="Updating a group by uuid without affecting the students"
                        " of the group and teachers and academic subjects",
            summary="Edit only groups",
            status_code=status.HTTP_200_OK, )
async def edit_only_groups(uow: UOWDep, groups_schema: SGroupsEdit, groups_uuid: UUID):
    """
    Updating a group without affecting its dependent entities
    """
    group_model = await GroupsService().updating_a_group_without_affecting_its_dependent_entities(
        uow, groups_schema, groups_uuid)
    return group_model


@router.delete('/{groups_uuid}',
               status_code=status.HTTP_200_OK,
               summary="Delete groups by UUID")
async def delete_groups(uow: UOWDep, groups_uuid: UUID):
    """
    Remove groups by UUID
    """
    await GroupsService().delete_groups_by_UUID(uow, groups_uuid)


@router.delete('/{subjects_uuid}/{groups_uuid}/subjects',
               status_code=status.HTTP_200_OK,
               summary="Delete subjects from groups by UUID")
async def delete_subjects_from_groups(uow: UOWDep,
                                      groups_uuid: UUID,
                                      subjects_uuid: UUID):
    """
    Deleting educational items from a group by UUID
    """
    await GroupsService().service_delete_subjects_from_groups(uow, subjects_uuid, groups_uuid)


@router.delete('/{teachers_uuid}/{groups_uuid}/teachers',
               status_code=status.HTTP_200_OK,
               summary="Delete teachers from groups by UUID")
async def delete_teachers_from_groups(uow: UOWDep, groups_uuid: UUID, teachers_uuid: UUID):
    """
    Removing teachers from a group by UUID
    """
    await GroupsService().service_delete_teachers_from_groups(uow, teachers_uuid, groups_uuid)


@router.delete('/{students_uuid}/{groups_uuid}/students',
               status_code=status.HTTP_200_OK,
               summary="Delete students from groups by UUID")
async def delete_students_from_groups(uow: UOWDep, groups_uuid: UUID, students_uuid: UUID):
    """
    Removing students from a group by UUID
    """
    await GroupsService().service_delete_students_from_groups(uow, students_uuid, groups_uuid)


@router.get('/all', summary="Get all groups",
            status_code=status.HTTP_200_OK, )
async def all_groups(uow: UOWDep):
    """
    Get all groups without students, without teachers and without subjects
    """
    groups = await GroupsService().get_groups_without_students_and_teachers_and_subjects(uow)
    return groups


@router.get('/all/subjects', summary="Get all groups with subjects",
            status_code=status.HTTP_200_OK, )
async def all_groups_with_subjects(uow: UOWDep):
    """
    Get all groups with academic subjects
    """
    groups_with_subjects = await GroupsService().get_groups_with_subjects(uow)
    return groups_with_subjects


@router.get('/all/students', summary="Get all groups with students",
            status_code=status.HTTP_200_OK, )
async def all_groups_with_students(uow: UOWDep):
    """
    Get all groups with students
    """
    groups_with_students = await GroupsService().get_groups_with_students(uow)
    return groups_with_students


@router.get('/all/teachers', summary="Get all groups with teachers",
            status_code=status.HTTP_200_OK, )
async def all_groups_with_teachers(uow: UOWDep):
    """
    Get all groups with teachers
    """
    groups_with_teachers = await GroupsService().get_groups_with_teachers(uow)
    return groups_with_teachers
