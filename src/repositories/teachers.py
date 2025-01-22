from utils.repository import SQLAlchemyRepository
from models.teachers import Teachers


class TeachersRepository(SQLAlchemyRepository):
    model = Teachers
