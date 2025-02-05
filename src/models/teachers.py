from models.dependencies_for_models import (uuid_pk, unique_required_name,
                                            required_name, optional_line)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum, DateTime
from schemas.teachers import STeachers
from datetime import datetime
from typing import List
from db.db import Base
from enum import Enum


class EnumTeachers(Enum):
    professor = "professor"
    associate_professor = "associate_professor"
    senior_lecturer = "senior_lecturer"
    assistant = "assistant"


class Teachers(Base):
    __tablename__ = 'teachers'
    uuid: Mapped[uuid_pk]
    first_name: Mapped[required_name]
    last_name: Mapped[required_name]
    middle_name: Mapped[optional_line]
    login: Mapped[unique_required_name]
    hashed_password: Mapped[required_name]
    is_role: Mapped[str] = mapped_column(SQLEnum(EnumTeachers), nullable=False, default=EnumTeachers.senior_lecturer)
    is_active: Mapped[int] = mapped_column(default=1, nullable=False)
    created_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    subjects: Mapped[List["Subjects"]] = relationship(back_populates="teachers",
                                                      secondary='teachers_subjects')
    groups: Mapped[List["Groups"]] = relationship(back_populates="teachers",
                                                  secondary="teachers_groups")

    def to_read_model(self) -> STeachers:
        return STeachers(uuid=self.uuid,
                         first_name=self.first_name,
                         last_name=self.last_name,
                         middle_name=self.middle_name,
                         login=self.login,
                         hashed_password=self.hashed_password,
                         is_role=self.is_role,
                         is_active=self.is_active,
                         created_on=self.created_on,
                         updated_on=self.updated_on,)
