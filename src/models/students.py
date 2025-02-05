from models.dependencies_for_models import (uuid_pk, required_name, unique_required_name, optional_line)
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import ForeignKey, DateTime, Enum as SQLEnum
from schemas.students import SStudents
from datetime import datetime
from db.db import Base
from uuid import UUID
from enum import Enum
from . import groups


class EnumStudents(Enum):
    student = "student"
    headman = "headman"


class Students(Base):
    __tablename__ = "students"
    uuid: Mapped[uuid_pk]
    first_name: Mapped[required_name]
    last_name: Mapped[required_name]
    middle_name: Mapped[optional_line]
    login: Mapped[unique_required_name]
    hashed_password: Mapped[required_name]
    faculty: Mapped[optional_line]
    is_role: Mapped[str] = mapped_column(SQLEnum(EnumStudents), nullable=False, default=EnumStudents.student)
    is_active: Mapped[int] = mapped_column(default=1, nullable=False)
    created_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    group_uuid: Mapped[UUID] = mapped_column(ForeignKey('groups.uuid', ondelete="CASCADE"), nullable=True)
    groups: Mapped["Groups"] = relationship(back_populates='students')

    def to_read_model(self) -> SStudents:
        return SStudents(uuid=self.uuid,
                         first_name=self.first_name,
                         last_name=self.last_name,
                         middle_name=self.middle_name,
                         login=self.login,
                         hashed_password=self.hashed_password,
                         is_role=self.is_role,
                         is_active=self.is_active,
                         created_on=self.created_on,
                         updated_on=self.updated_on,
                         group_uuid=self.group_uuid,
                         )
