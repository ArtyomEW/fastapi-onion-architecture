from schemas.subjects import SSubjectsAdd
from utils.unitofwork import UnitOfWork
from core.exceptions import MyException
from uuid import UUID


class SubjectsService:

    # @classmethod
    # async def add_subjects(cls, uow: UnitOfWork, subjects_schema: SSubjectsAdd):
    #     async with uow:
    #         subjects = await uow.subjects.add_one()

    @staticmethod
    async def get_subjects_with_filter_uuid(uow: UnitOfWork, uuid: UUID):
        """
        Находим предмет по UUID
        """
        try:
            async with uow:
                subjects = await uow.subjects.find_all_with_filer({"uuid": uuid})
                return subjects[0]
        except Exception as e:
            MyException(status_code=409, message=f"Исключение в get_subjects_with_filter_uuid {e}")
