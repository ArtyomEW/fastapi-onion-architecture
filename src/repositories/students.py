from utils.repository import SQLAlchemyRepository
from models.students import Students


class StudentsRepository(SQLAlchemyRepository):
    model = Students
