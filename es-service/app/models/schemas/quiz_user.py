from typing import Optional

from app.models.common import SchemaBase


class QuizUserBase(SchemaBase):
    answer: Optional[str] = None


class JoinQuizRequest(QuizUserBase):
    user_id: Optional[int]
    quiz_id: Optional[int]
    pass


class SubmitAnswerRequest(SchemaBase):
    answer: str
