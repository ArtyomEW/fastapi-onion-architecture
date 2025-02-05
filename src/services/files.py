from utils.unitofwork import UnitOfWork
from core.exceptions import MyException
from fastapi import UploadFile
from pprint import pprint
from uuid import UUID


class FilesService:

    @staticmethod
    async def add_file(uow: UnitOfWork, file: UploadFile,
                       groups_uuid: UUID, subjects_uuid: UUID):
        """
        Конвертируем файл в bytes и
        добавляем в базу данных
        """
        try:
            file_bytes = await file.read()
        except Exception as e:
            pprint(e)
            raise MyException(status_code=409, message="Исключение в add_file. "
                                                       "При чтении файла произошла ошибка")
        data_file = {
            "file_name": file.filename,
            "mime_type": file.content_type.split('/')[-1],
            "file_data": file_bytes,
            "subjects_uuid": subjects_uuid,
            "groups_uuid": groups_uuid,
        }
        async with uow:
            try:
                await uow.files.add_one(data_file)
                await uow.commit()
            except Exception as e:
                pprint(e)
                raise MyException(status_code=500, message="Исключение в add_file. "
                                                           "После uow.commit произошла ошибка")

    @staticmethod
    async def delete_files_by_UUID(uow: UnitOfWork, files_uuid: UUID):
        """
        Delete a file by UUID
        """
        async with uow:
            try:
                await uow.files.delete({"uuid": files_uuid})
                await uow.commit()
            except Exception as e:
                pprint(e)
                raise MyException(status_code=409, message="Исключение в delete_files_by_UUID")

    @staticmethod
    async def get_files_by_uuid(uow: UnitOfWork, files_uuid: UUID):
        """
        Get file by UUID
        """
        async with uow:
            file_model = await uow.files.find_one({"uuid": files_uuid})
            if not file_model:
                raise MyException(status_code=409, message="Исключение в get_file_by_uuid "
                                                           "Нету такого файла")
            try:
                with open(f'storage/files/{file_model.file_name}.{file_model.mime_type}', 'wb') as file:
                    file.write(file_model.file_data)
            except Exception as e:
                pprint(e)
                raise MyException(status_code=500, message="Исключение в get_files_by_uuid. "
                                                           "При сохранении файла произошла ошибка")
