from utils.repository import SQLAlchemyRepository
from models.groups import Groups


class GroupsRepository(SQLAlchemyRepository):
    model = Groups
