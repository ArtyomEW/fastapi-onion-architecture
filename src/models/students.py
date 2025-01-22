from models.dependencies_for_models import uuid_pk, required_name, unique_required_name, optional_line
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
    name: Mapped[required_name]
    surname: Mapped[required_name]
    father_name: Mapped[optional_line]
    login: Mapped[unique_required_name]
    hashed_password: Mapped[required_name]
    faculty: Mapped[optional_line]
    is_role: Mapped[str] = mapped_column(SQLEnum(EnumStudents), nullable=False, default=EnumStudents.student)
    is_active: Mapped[int] = mapped_column(default=1, nullable=False)
    created_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    group_uuid: Mapped[UUID] = mapped_column(ForeignKey('groups.uuid', ondelete="CASCADE"), nullable=True)
    groups: Mapped["Groups"] = relationship(back_populates='students')

    # def __repr__(self):
    #     return (f"Students({self.uuid}, {self.name}, {self.surname}, {self.father_name}, {self.login}, {self.hashed_password}, "
    #             f"{self.faculty}, {self.is_role}, {self.is_active}, {self.created_on}, {self.updated_on}, "
    #             f"{self.group_uuid}), {self.groups}")

    def to_read_model(self) -> SStudents:
        return SStudents(uuid=self.uuid,
                         name=self.name,
                         surname=self.surname,
                         father_name=self.father_name,
                         login=self.login,
                         hashed_password=self.hashed_password,
                         is_role=self.is_role,
                         is_active=self.is_active,
                         created_on=self.created_on,
                         updated_on=self.updated_on,
                         group_uuid=self.group_uuid,
                          )
