from schemas.groups import SGroupsAdd, SGroups
from fastapi import APIRouter, status, Depends
from services.groups import GroupsService
from api.dependencies import UOWDep
from typing import Annotated

router = APIRouter(prefix='/groups',
                   tags=['Groups'])


@router.post('/', description="Add groups",
             status_code=status.HTTP_201_CREATED,
             )
async def add_groups(uow: UOWDep, groups_schema: Annotated[SGroupsAdd, Depends()]):
    group_uuid = await GroupsService().add_groups(uow, groups_schema)
    return {"group_uuid": group_uuid}


@router.get('/all_groups', description='get all groups',
            status_code=status.HTTP_200_OK,
            response_model=list[SGroups],
            response_model_exclude_unset=True)
async def all_groups(uow: UOWDep):
    groups = await GroupsService().get_only_groups(uow)
    return groups


