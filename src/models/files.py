from models.dependencies_for_models import uuid_pk, required_name
from sqlalchemy import LargeBinary, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from schemas.files import SFiles
from . import subjects, groups
from datetime import datetime
from db.db import Base
from uuid import UUID


class Files(Base):
    __tablename__ = 'files'
    uuid: Mapped[uuid_pk]
    file_name: Mapped[required_name]
    mime_type: Mapped[required_name]
    file_data: Mapped[bytes] = mapped_column(LargeBinary)  # Соответствует bytea в PostgreSQL
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    subjects_uuid: Mapped[UUID] = mapped_column(ForeignKey('subjects.uuid', ondelete="CASCADE"), nullable=False)
    groups_uuid: Mapped[UUID] = mapped_column(ForeignKey('groups.uuid', ondelete="CASCADE"), nullable=False)

    def to_read_model(self) -> SFiles:
        return SFiles(file_name=self.file_name,
                      mime_type=self.mime_type,
                      uploaded_at=self.uploaded_at,
                      subject_uuid=self.subjects_uuid,
                      group_uuid=self.groups_uuid, )
