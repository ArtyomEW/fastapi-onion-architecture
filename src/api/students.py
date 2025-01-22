from fastapi import APIRouter, status, Depends
from services.students import StudentsService
from schemas.students import SStudentsAdd
from api.dependencies import UOWDep
from typing import Annotated

router = APIRouter(
    prefix="/students",
    tags=["Student"],
)


@router.post("", description="Add students with their groups",
             status_code=status.HTTP_201_CREATED)
async def add_students(
        student_schema: Annotated[SStudentsAdd, Depends()],
        uow: UOWDep,
):
    student_model = await StudentsService().add_student(uow, student_schema)
    return student_model


@router.get("/specific",
            description="Displays all students with their groups",
            status_code=status.HTTP_200_OK,
            summary="get_student_by_uuid",
            )
async def get_student_by_uuid(
    uow: UOWDep,
):
    students = await StudentsService().get_subjects_and_teachers(uow, '976ebc31-7bab-4314-8ce8-b5ba01ec1dcf')
    return students
