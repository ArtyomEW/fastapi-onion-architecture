from schemas.teachers import (STeacherAdd, STeachersEdit,
                              STeachersSubjects, STeachersGroups)
from fastapi import APIRouter, status, Depends
from services.teachers import TeachersService
from api.dependencies import UOWDep
from typing import Annotated
from uuid import UUID

router_teachers = APIRouter(
    prefix='/admin/teachers',
    tags=['AdminTeachers']
)


@router_teachers.post('/', status_code=status.HTTP_201_CREATED,
                      summary='Add teachers without groups and without subjects')
async def add_teachers(uow: UOWDep, teachers_schema_add: Annotated[STeacherAdd, Depends()]):
    """
    Adding a teacher without groups and subjects
    """
    teachers = await TeachersService().add_teachers(uow, teachers_schema_add)
    return teachers


@router_teachers.post("/subjects/{teachers_uuid}",
                      status_code=status.HTTP_201_CREATED,
                      summary="Add subjects to teacher")
async def add_subjects_to_teachers(uow: UOWDep, teachers_uuid: UUID,
                                   subjects_uuid: STeachersSubjects):
    """
    Add school items to teacher
    """
    await TeachersService().add_subjects_by_teachers(uow, subjects_uuid, teachers_uuid)


@router_teachers.post("/groups/{teachers_uuid}",
                      status_code=status.HTTP_201_CREATED,
                      summary="Add groups to teacher")
async def add_groups_to_teachers(uow: UOWDep, teachers_uuid: UUID,
                                 groups_uuid: STeachersGroups):
    await TeachersService().add_groups_by_teachers(uow, groups_uuid, teachers_uuid)


@router_teachers.put("/{teachers_uuid}",
                     status_code=status.HTTP_200_OK,
                     summary="Edit teachers without groups and subjects",
                     description="Updating a teacher by his uuid",
                     )
async def put_teacher(uow: UOWDep,
                      teachers_uuid: UUID,
                      teachers_schema_put: Annotated[STeachersEdit, Depends()]):
    """
    Update the teacher without affecting his subjects and groups
    """
    await TeachersService().edit_only_teachers(uow, teachers_schema_put, teachers_uuid)


@router_teachers.delete('/{subjects_uuid}/{teachers_uuid}/subjects',
                        status_code=status.HTTP_200_OK,
                        summary="Remove a subject from a teacher")
async def delete_subjects_from_teachers(uow: UOWDep, teachers_uuid: UUID, subjects_uuid: UUID):
    """
    Removing a subject from a teacher
    """
    await TeachersService().delete_subjects_from_teachers(uow, subjects_uuid, teachers_uuid)


@router_teachers.delete('/{groups_uuid}/{teachers_uuid}/groups',
                        status_code=status.HTTP_200_OK,
                        summary="Remove a group from a teacher")
async def delete_groups_from_teachers(uow: UOWDep, teachers_uuid: UUID, groups_uuid: UUID):
    """
    Delete a teacher's group by UUID
    """
    await TeachersService().delete_groups_from_teachers(uow, groups_uuid, teachers_uuid)


@router_teachers.delete('/{teachers_uuid}',
                        status_code=status.HTTP_200_OK,
                        summary="Delete teachers by uuid")
async def delete_teachers(uow: UOWDep, teachers_uuid: UUID):
    """
    Removing a teacher by uuid
    """
    await TeachersService().delete_teacher(uow, teachers_uuid)


@router_teachers.get('/all',
                     status_code=status.HTTP_200_OK,
                     summary="Get all teachers without their subjects and groups")
async def get_all_teachers(uow: UOWDep):
    """
    Get all teachers without academic subjects
    """
    data_teachers = await TeachersService().get_all_teachers(uow)
    return data_teachers


@router_teachers.get('/all/groups',
                     status_code=status.HTTP_200_OK,
                     summary="Get all teachers with groups")
async def get_all_teachers_with_groups(uow: UOWDep):
    """
    Get all teachers with their groups
    """
    data_teachers = await TeachersService().get_all_teachers_with_groups(uow)
    return data_teachers


@router_teachers.get('/all/subjects', status_code=status.HTTP_200_OK,
                     summary="Get all teachers with subjects")
async def get_all_teachers_with_subjects(uow: UOWDep):
    """
    Get all teachers with their academic subjects
    """
    data_teachers = await TeachersService().get_all_teachers_with_subjects(uow)
    return data_teachers
