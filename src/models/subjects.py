from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.dependencies_for_models import uuid_pk
from schemas.subjects import SSubjects
from . import groups, teachers
from typing import List
from db.db import Base


class Subjects(Base):
    __tablename__ = 'subjects'
    uuid: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    groups: Mapped[List["Groups"]] = relationship(back_populates="subjects", secondary="groups_subjects")
    teachers: Mapped[List["Teachers"]] = relationship(back_populates="subjects", secondary="teachers_subjects")

    def to_read_model(self) -> SSubjects:
        return SSubjects(
            uuid=self.uuid,
            name=self.name,)
