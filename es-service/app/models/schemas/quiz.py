from datetime import datetime
from typing import Optional

from app.models.common import SchemaBase


class QuizBase(SchemaBase):
    name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
