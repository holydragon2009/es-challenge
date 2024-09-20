from datetime import datetime
import json

import pydantic
from pydantic import BaseModel

from sqlalchemy import text, Column, Boolean, DateTime
from sqlalchemy.orm import declared_attr


class SchemaBase(BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)


class EmptyBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class DeactivatedModel(EmptyBase):
    deactivated = Column(Boolean, default=False)


class TimestampModel(EmptyBase):
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=text("current_timestamp(0)"))


class JsonObjectMixin(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


