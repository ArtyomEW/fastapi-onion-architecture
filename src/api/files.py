from fastapi import APIRouter, status, UploadFile
from services.files import FilesService
from .dependencies import UOWDep
from uuid import UUID

router = APIRouter(
    prefix='/files',
    tags=['files'])


@router.post('/{groups_uuid}/{subjects_uuid}',
             status_code=status.HTTP_200_OK,
             summary="Add file")
async def add_file(uow: UOWDep, file: UploadFile,
                   groups_uuid: UUID, subjects_uuid: UUID):
    """
    Add a file to a specific group and object by UUID
    """
    await FilesService().add_file(uow, file, groups_uuid, subjects_uuid)


@router.post('/{files_uuid}',
             status_code=status.HTTP_200_OK,
             summary="Get files by UUID")
async def get_files_by_uuid(uow: UOWDep, files_uuid: UUID):
    """
    Get file by UUID
    """
    await FilesService().get_files_by_uuid(uow, files_uuid)


@router.delete('/{files_uuid}',
               status_code=status.HTTP_200_OK,
               summary="Delete file by UUID")
async def delete_files_by_uuid(uow: UOWDep, files_uuid: UUID):
    """
    Delete a file by UUID
    """
    await FilesService().delete_files_by_UUID(uow, files_uuid)
