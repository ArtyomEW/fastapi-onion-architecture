from models.dependencies_for_models import uuid_pk, unique_required_name
from sqlalchemy.orm import relationship, Mapped
from . import students, subjects, teachers, m2m
from schemas.groups import SGroups
from typing import List
from db.db import Base


class Groups(Base):
    __tablename__ = 'groups'
    uuid: Mapped[uuid_pk]
    number_group: Mapped[unique_required_name]
    subjects: Mapped[List["Subjects"]] = relationship(back_populates="groups", secondary="groups_subjects")
    teachers: Mapped[List["Teachers"]] = relationship(back_populates='groups', secondary="teachers_groups")
    students: Mapped[List["Students"]] = relationship(back_populates='groups')

    def to_read_model(self) -> SGroups:
        return SGroups(uuid=self.uuid,
                       number_group=self.number_group, )
