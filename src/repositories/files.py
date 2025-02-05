from utils.repository import SQLAlchemyRepository
from models.files import Files


class FilesRepository(SQLAlchemyRepository):
    model = Files
