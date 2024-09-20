import typing
from datetime import datetime

import sqlalchemy as sa
from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import orm, text
from sqlalchemy.orm import Mapped, mapped_column

METADATA: typing.Final = sa.MetaData()
orm.DeclarativeBase.metadata = METADATA


class User(
    BigIntAuditBase,
):
    __tablename__ = 'user'

    email: Mapped[str] = mapped_column(sa.String, unique=True, index=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    avatar: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    salt: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    hashed_password: Mapped[str] = mapped_column(sa.String)
    deactivated: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow, nullable=False,
                                                 onupdate=text("current_timestamp(0)"))




