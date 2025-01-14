from models.dependencies_for_models import intpk, required_name, unique_required_name
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import ForeignKey, Enum as SQLEnum, DateTime
from schemas.students import SStudents
from datetime import datetime
from db.db import Base

from enum import Enum


class EnumRole(Enum):
    student = "student"
    headman = "headman"


class Students(Base):
    __tablename__ = "students"
    id: Mapped[intpk]
    name: Mapped[required_name]
    surname: Mapped[required_name]
    father_name: Mapped[str | None] = mapped_column(default=None, nullable=True)
    login: Mapped[unique_required_name]
    hashed_password: Mapped[required_name]
    is_role: Mapped[str] = mapped_column(SQLEnum(EnumRole), nullable=False, default=EnumRole.student)
    is_active: Mapped[int] = mapped_column(default=1, nullable=False)
    created_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    group_id: Mapped[intpk] = mapped_column(ForeignKey('groups.id', ondelete="CASCADE"), nullable=True)
    groups: Mapped["Groups"] = relationship(back_populates='students')

    def to_read_model(self) -> SStudents:
        return SStudents(id=self.id,
                         name=self.name,
                         surname=self.surname,
                         father_name=self.father_name,
                         hashed_password=self.hashed_password,
                         is_role=self.is_role,
                         is_active=self.is_active,
                         created_on=self.created_on,
                         updated_on=self.updated_on,
                         group_id=self.group_id,
                         groups=self.groups, )
