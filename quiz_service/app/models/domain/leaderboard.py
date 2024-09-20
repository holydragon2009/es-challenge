from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from app.models.common import TimestampModel, DeactivatedModel
from app.models.domain.quiz import Quiz
from app.models.domain.user import User


class LeaderboardBase(SQLModel):
    score: int


class Leaderboard(
    LeaderboardBase,
    TimestampModel,
    DeactivatedModel,
    table=True
):
    __tablename__ = 'leaderboard'
    quiz_id: Optional[int] = Field(default=None, nullable=False, foreign_key="quiz.quiz_id", primary_key=True)
    user_id: Optional[int] = Field(default=None, nullable=False, foreign_key="user.user_id", primary_key=True)
    score: int = Field(..., index=True)

    user: Optional[User] = Relationship(back_populates="leaderboard_entries")
    quiz: Optional[Quiz] = Relationship(back_populates="leaderboard_entries")


class UpdateScoreRequest(LeaderboardBase):
    user_id: Optional[int]
    quiz_id: Optional[int]
    pass
