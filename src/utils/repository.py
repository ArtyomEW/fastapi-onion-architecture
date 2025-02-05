from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from uuid import UUID

class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError
    
    @abstractmethod
    async def find_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        res = res.scalars().all()
        return res

    async def edit_one(self, uuid: UUID, data: dict):
        stmt = update(self.model).values(**data).filter_by(uuid=uuid)
        await self.session.execute(stmt)

    async def find_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res
    
    async def find_all_with_filer(self, filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalars().all()
        return res

    async def delete(self, filter_by):
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)

    async def find_one(self, filter_by, ):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalars().first()
        return res
