from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from typing import Annotated
from uuid import UUID, uuid4

uuid_pk = Annotated[UUID, mapped_column(primary_key=True, default=uuid4)]
required_name = Annotated[str, mapped_column(nullable=False)]
unique_required_name = Annotated[str, mapped_column(String(100), nullable=False, unique=True)]
optional_line = Annotated[str | None, mapped_column(default=None, nullable=True)]
