from datetime import datetime

import sqlalchemy as sa
from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column


class Quiz(
    BigIntAuditBase,
):
    __tablename__ = 'quiz'

    deactivated: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow, nullable=False,
                                                 onupdate=text("current_timestamp(0)"))