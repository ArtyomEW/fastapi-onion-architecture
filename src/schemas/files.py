from .dependencies_for_schemas import BaseSchema, Field
from datetime import datetime


class SFiles(BaseSchema):
    file_name: str
    mime_type: str
    uploaded_at: datetime
    subject_uuid: str
    group_uuid: str | None = Field(default=None)
