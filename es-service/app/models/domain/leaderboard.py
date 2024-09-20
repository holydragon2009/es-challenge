from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base


class Leaderboard(
    Base,
):
    __tablename__ = 'leaderboard'

    quiz_id: Mapped[int] = mapped_column(sa.INT, nullable=False, foreign_key="quiz.id", primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.INT, nullable=False, foreign_key="user.id", primary_key=True)

    score: Mapped[int] = mapped_column(sa.INT, default=0, index=True)

    deactivated: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow, nullable=False,
                                                 onupdate=text("current_timestamp(0)"))

