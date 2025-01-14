from models.dependencies_for_models import intpk, unique_required_name, required_name
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum, DateTime
from schemas.teachers import STeachers
from datetime import datetime
from typing import List
from db.db import Base
from enum import Enum


class EnumRole(Enum):
    professor = "professor"
    associate_professor = "associate_professor"
    senior_lecturer = "senior_lecturer"
    assistant = "assistant"


class Teachers(Base):
    __tablename__ = 'teachers'
    id: Mapped[intpk]
    name: Mapped[required_name]
    surname: Mapped[required_name]
    father_name: Mapped[str] = mapped_column(nullable=True)
    login: Mapped[unique_required_name]
    hashed_password: Mapped[required_name]
    is_role: Mapped[str] = mapped_column(SQLEnum(EnumRole), nullable=False, default=EnumRole.senior_lecturer)
    is_active: Mapped[int] = mapped_column(default=1, nullable=False)
    created_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    subjects: Mapped[List["Subjects"]] = relationship(back_populates="teachers", secondary='teachers_subjects')
    groups: Mapped[List["Groups"]] = relationship(back_populates="teachers", secondary="teachers_groups")

    def to_read_model(self) -> STeachers:
        return STeachers(id=self.id,
                         name=self.name,
                         surname=self.surname,
                         father_name=self.father_name,
                         login=self.login,
                         hashed_password=self.hashed_password,
                         is_role=self.is_role,
                         is_active=self.is_active,
                         created_on=self.created_on,
                         updated_on=self.updated_on,
                         subjects=self.subjects,
                         groups=self.groups,)
