from utils.repository import SQLAlchemyRepository
from models.subjects import Subjects


class SubjectsRepository(SQLAlchemyRepository):
    model = Subjects
