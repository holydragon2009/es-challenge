from typing import List, Optional

from sqlmodel import select, or_, col, Session

from app.db.repositories.base_repo import BaseRepo
from app.models.domain.quiz import JoinQuizRequest, Quiz


class QuizRepository(BaseRepo):

    async def create(self, data: JoinQuizRequest) -> Quiz:
        quiz = Quiz(
            quiz_id=data.quiz_id,
            user_id=data.user_id
        )
        self._session.add(quiz)
        await self._session.commit()
        await self._session.refresh(quiz)
        return quiz

    async def get(self, quiz_id: int, user_id: int) -> Quiz:
        statement = select(Quiz).where(Quiz.quiz_id == quiz_id).where(Quiz.user_id == user_id).where(Quiz.deactivated == False)
        results = await self._session.execute(statement=statement)
        team = results.scalar_one_or_none()  # type: Quiz | None
        return team

    async def update(self, user_id: int, quiz_id: int, answers: List[str]) -> Quiz:
        quiz = Quiz(
            quiz_id=quiz_id,
            user_id=user_id,
            answers=answers
        )
        self._session.add(quiz)
        await self._session.commit()
        await self._session.refresh(quiz)
        return quiz
