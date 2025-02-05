from schemas.subjects import (SSubjectsAdd, SSubjectsGroups, SSubjectsTeachers, SSubjectsEdit)
from fastapi import APIRouter, status, Depends
from services.subjects import SubjectsService
from api.dependencies import UOWDep
from typing import Annotated
from uuid import UUID

router = APIRouter(
    prefix='/admin/subjects',
    tags=['AdminSubjects']
)


@router.post('/',
             status_code=status.HTTP_201_CREATED,
             description='Add subjects with their teachers and groups',
             summary='add_subjects')
async def add_subjects(uow: UOWDep, subjects_schema: Annotated[SSubjectsAdd, Depends()]):
    """
    Adding educational
    item to the database.
    """
    subjects = await SubjectsService().add_subjects(uow, subjects_schema)
    return subjects


@router.post('/groups/{subjects_uuid}',
             status_code=status.HTTP_201_CREATED,
             description='Add groups to subjects',
             summary='Add groups to subjects')
async def add_groups_to_subjects(uow: UOWDep, subjects_uuid: UUID, groups_uuid: SSubjectsGroups):
    """
    Adding groups to a subject by UUID
    """
    subjects = await SubjectsService().add_groups_to_subjects(uow, groups_uuid, subjects_uuid)
    return subjects


@router.post('/teachers/{subjects_uuid}',
             status_code=status.HTTP_201_CREATED,
             description='Add teachers to subjects',
             summary='Add teachers to subjects')
async def add_teachers_to_subjects(uow: UOWDep, subjects_uuid: UUID, teachers_uuid: SSubjectsTeachers):
    """
    Adding teachers to a subject
    """
    subjects = await SubjectsService().add_teachers_to_subjects(uow, teachers_uuid, subjects_uuid)
    return subjects


@router.put("/{subjects_uuid}",
            status_code=status.HTTP_200_OK,
            summary="Edit subjects without groups and teachers",
            description="Updating a subject by his uuid",
            )
async def put_subjects(uow: UOWDep,
                       subjects_uuid: UUID,
                       subjects_schema_put: Annotated[SSubjectsEdit, Depends()]):
    """
    We update a subject without its teachers and groups
    """
    await SubjectsService().edit_only_subjects(uow, subjects_schema_put, subjects_uuid)


@router.delete('/{subjects_uuid}')
async def delete_subjects_by_uuid(uow: UOWDep, subjects_uuid: UUID):
    """
    Remove subjects by UUID
    """
    await SubjectsService().delete_subjects(uow, subjects_uuid)


@router.delete('/{groups_uuid}/{subjects_uuid}/groups')
async def delete_groups_from_subjects_by_uuid(uow: UOWDep, subjects_uuid: UUID, groups_uuid: UUID):
    """
    Delete a group from an academic subject by UUID
    """
    await SubjectsService().delete_groups_from_subjects(uow, groups_uuid, subjects_uuid)


@router.delete('/{teachers_uuid}/{subjects_uuid}/teacher')
async def delete_teachers_from_subjects_by_uuid(uow: UOWDep, subjects_uuid: UUID, teachers_uuid: UUID):
    """
    Removing a teacher from a subject by UUID
    """
    await SubjectsService().delete_teachers_from_subjects(uow, teachers_uuid, subjects_uuid)


@router.get('/all', status_code=status.HTTP_200_OK,
            summary='Get all subjects')
async def get_all_subjects(uow: UOWDep):
    """
    Get all educational items
    """
    all_subjects = await SubjectsService().get_all_subjects_without_groups_and_teachers(uow)
    return all_subjects


@router.get('/all/groups', status_code=status.HTTP_200_OK,
            summary="Get all subjects with groups")
async def get_all_subjects_with_groups(uow: UOWDep):
    """
    Get all teachers with their groups
    """
    data_subjects = await SubjectsService().get_all_subjects_with_groups(uow)
    return data_subjects


@router.get('/all/teachers', status_code=status.HTTP_200_OK,
            summary="Get all subjects with teachers")
async def get_all_subjects_with_teachers(uow: UOWDep):
    """
    Get all teachers with their teachers
    """
    data_subjects = await SubjectsService().get_all_subjects_with_teachers(uow)
    return data_subjects
