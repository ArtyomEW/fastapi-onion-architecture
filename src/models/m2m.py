from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from db.db import Base


class groups_subjects(Base):
    __tablename__ = "groups_subjects"
    groups_id: Mapped[int] = mapped_column(ForeignKey('groups.id', ondelete="CASCADE"), primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id', ondelete="CASCADE"), primary_key=True)


class teachers_subjects(Base):
    __tablename__ = "teachers_subjects"
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id', ondelete="CASCADE"), primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id', ondelete="CASCADE"), primary_key=True)


class teachers_groups(Base):
    __tablename__ = "teachers_groups"
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id', ondelete="CASCADE"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id', ondelete="CASCADE"), primary_key=True)
