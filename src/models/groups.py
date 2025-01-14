from models.dependencies_for_models import intpk, unique_required_name
from sqlalchemy.orm import relationship, Mapped, mapped_column
from schemas.groups import SGroups
from typing import List
from db.db import Base


class Groups(Base):
    __tablename__ = 'groups'
    id: Mapped[intpk]
    number_group: Mapped[unique_required_name]
    faculty: Mapped[str | None] = mapped_column(default=None, nullable=True)
    subjects: Mapped[List["Subjects"]] = relationship(back_populates="groups", secondary="groups_subjects")
    teachers: Mapped[List["Teachers"]] = relationship(back_populates='groups', secondary="teachers_groups")
    students: Mapped[List["Students"]] = relationship(back_populates='groups')

    def to_read_model(self) -> SGroups:
        return SGroups(id=self.id,
                       number_group=self.number_group,
                       faculty=self.faculty,
                       subjects=self.subjects,
                       teachers=self.teachers,
                       students=self.students, )
