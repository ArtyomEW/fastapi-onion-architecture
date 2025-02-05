from schemas.students import SStudentsAdd, SStudentsGroups, SStudentsEdit
from services.students import StudentsService
from fastapi import APIRouter, Depends
from api.dependencies import UOWDep
from typing import Annotated
from starlette import status
from uuid import UUID

router_admin_students = APIRouter(
    prefix='/admin/students',
    tags=['AdminStudents']
)


@router_admin_students.post("", description="Add students without groups",
                            summary="Add students without groups",
                            status_code=status.HTTP_201_CREATED)
async def add_students(
        student_schema: Annotated[SStudentsAdd, Depends()],
        uow: UOWDep,
):
    """
    Adding a student without a group
    """
    student_model = await StudentsService().add_student(uow, student_schema)
    return student_model


@router_admin_students.post('/groups/{students_uuid}',
                            status_code=status.HTTP_200_OK,
                            summary="Assign a group to a student",
                            description="If we assign a new group then the student will be in a new")
async def assign_a_group_to_a_student(uow: UOWDep, groups_schema: SStudentsGroups, students_uuid: UUID):
    """
    If we assign a new group
    then the student will be in a new
    """
    await StudentsService().add_groups_to_students(uow, groups_schema, students_uuid)


@router_admin_students.put('/{students_uuid}',
                           status_code=status.HTTP_200_OK,
                           summary="Update student by UUID",
                           description="We update the student by UUID but we cannot touch his group")
async def update_student_by_UUID(uow: UOWDep, students_schema: SStudentsEdit, students_uuid: UUID):
    """
    Update student by UUID
    """
    await StudentsService().update_students_by_UUID(uow, students_schema, students_uuid)


@router_admin_students.delete('/{students_uuid}',
                              status_code=status.HTTP_200_OK,
                              summary="Removing a student by UUID")
async def delete_students(uow: UOWDep, students_uuid: UUID):
    """
    Removing a student by UUID
    """
    await StudentsService().delete_students(uow, students_uuid)


@router_admin_students.delete('/{groups_uuid}/{students_uuid}/groups',
                              status_code=status.HTTP_200_OK,
                              summary="Removing a group from a student by UUID")
async def removing_a_group_from_a_student(uow: UOWDep, students_uuid: UUID, groups_uuid: UUID):
    """
    Removing a group from a student by UUID
    """
    await StudentsService().delete_groups_from_students(uow, students_uuid, groups_uuid)


@router_admin_students.get("/all",
                           description="Get all students but without their groups",
                           status_code=status.HTTP_200_OK,
                           summary="Get all students",
                           )
async def get_all_students(
        uow: UOWDep,
):
    """
    Get all students but without their groups
    """
    students = await StudentsService().get_only_students(uow)
    return students
