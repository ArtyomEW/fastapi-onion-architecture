from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)

    class Config:
        from_attributes = True
