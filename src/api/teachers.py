from schemas.teachers import (STeacherAdd, STeachersEdit,
                              STeachersSubjects, STeachersGroups)
from fastapi import APIRouter, status, Depends
from services.teachers import TeachersService
from api.dependencies import UOWDep
from typing import Annotated
from uuid import UUID

router = APIRouter(prefix='/teachers', tags=['Teachers'])

