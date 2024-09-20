from datetime import datetime
import json

from pydantic import BaseModel

from sqlalchemy import text
from sqlmodel import Field, SQLModel


class DeactivatedModel(SQLModel):
    deactivated: bool = False


class TimestampModel(SQLModel):
   created_at: datetime = Field(
       default_factory=datetime.utcnow,
       nullable=False,
       sa_column_kwargs={
           "server_default": text("current_timestamp(0)")
       }
   )

   updated_at: datetime = Field(
       default_factory=datetime.utcnow,
       nullable=False,
       sa_column_kwargs={
           "server_default": text("current_timestamp(0)"),
           "onupdate": text("current_timestamp(0)")
       }
   )


class JsonObjectMixin(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


