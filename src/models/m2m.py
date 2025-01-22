from sqlalchemy.orm import Mapped, mapped_column
from . import groups, subjects, teachers
from sqlalchemy import ForeignKey
from db.db import Base


class groups_subjects(Base):
    __tablename__ = "groups_subjects"
    groups_uuid: Mapped[str] = mapped_column(ForeignKey('groups.uuid', ondelete="CASCADE"), primary_key=True)
    subject_uuid: Mapped[str] = mapped_column(ForeignKey('subjects.uuid', ondelete="CASCADE"), primary_key=True)


class teachers_subjects(Base):
    __tablename__ = "teachers_subjects"
    teacher_uuid: Mapped[str] = mapped_column(ForeignKey('teachers.uuid', ondelete="CASCADE"), primary_key=True)
    subject_uuid: Mapped[str] = mapped_column(ForeignKey('subjects.uuid', ondelete="CASCADE"), primary_key=True)


class teachers_groups(Base):
    __tablename__ = "teachers_groups"
    teacher_uuid: Mapped[str] = mapped_column(ForeignKey('teachers.uuid', ondelete="CASCADE"), primary_key=True)
    group_uuid: Mapped[str] = mapped_column(ForeignKey('groups.uuid', ondelete="CASCADE"), primary_key=True)
