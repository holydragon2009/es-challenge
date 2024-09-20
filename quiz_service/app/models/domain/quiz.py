from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from app.models.common import TimestampModel, DeactivatedModel
from app.models.domain.leaderboard import Leaderboard
from app.models.domain.user import User


class QuizBase(SQLModel):
    answers: Optional[List[str]] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class Quiz(
    QuizBase,
    TimestampModel,
    DeactivatedModel,
    table=True
):
    __tablename__ = 'quiz'
    quiz_id: int = Field(default=None, nullable=False, primary_key=True)
    user_id: Optional[int] = Field(default=None, nullable=False, foreign_key="user.user_id", primary_key=True)
    user: Optional[User] = Relationship(back_populates="quizzes")
    leaderboard_entries: List[Leaderboard] = Relationship(back_populates="quiz")


class JoinQuizRequest(QuizBase):
    user_id: Optional[int]
    quiz_id: Optional[int]
    pass


class SubmitAnswerRequest(SQLModel):
    answers: List[str]
