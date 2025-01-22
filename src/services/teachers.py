from utils.unitofwork import UnitOfWork
from core.exceptions import MyException


class TeachersService:
    @staticmethod
    async def get_teachers_with_filter_uuid(uow: UnitOfWork, uuid: str):
        """
        Находим учителя по UUID
        """
        try:
            async with uow:
                teachers = await uow.teachers.find_all_with_filer({'uuid': uuid})
                return teachers[0]
        except Exception as e:
            raise MyException(status_code=409, message=f"Исключение в get_teachers_with_filter_uuid - {e}. "
                                                       f"Возможно вы ввели не существующего преподавателя")
