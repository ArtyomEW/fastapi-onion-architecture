from services.students import StudentsService
from api.dependencies import UOWDep, limiter
from fastapi import APIRouter, status

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.get("/all/groups/teachers/subjects",
            description="Get all the students in their group, "
                        "their academic subjects and their teachers",
            status_code=status.HTTP_200_OK,
            summary="Get all students",
            )
@limiter.limit("5/minute")
async def get_all_students(
        uow: UOWDep,
):
    """
    Get all the students in their group,
    their academic subjects and their teachers
    """
    students = await StudentsService().get_students_subjects_and_teachers(uow)
    return students
