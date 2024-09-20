from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base


class QuizUser(
    Base,
):
    __tablename__ = 'quiz_user'

    quiz_id: Mapped[int] = mapped_column(sa.INT, nullable=False, foreign_key="quiz.id", primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.INT, nullable=False, foreign_key="user.id", primary_key=True)
    answer: Mapped[str | None] = mapped_column(sa.String, nullable=True)

    deactivated: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow, nullable=False,
                                                 onupdate=text("current_timestamp(0)"))



