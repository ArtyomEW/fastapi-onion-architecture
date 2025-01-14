from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]
required_name = Annotated[str, mapped_column(nullable=False)]
unique_required_name = Annotated[str, mapped_column(String(100), nullable=False, unique=True)]
