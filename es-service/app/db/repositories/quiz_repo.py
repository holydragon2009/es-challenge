from sqlmodel import select

from app.core.general import GeneralResponse
from app.db.repositories.base_repo import BaseRepo
from app.models.domain.quiz import Quiz
from app.models.domain.quiz_user import QuizUser


class QuizRepository(BaseRepo):

    async def create(self, user_id: int, quiz_id: int) -> Quiz:
        quiz_user = QuizUser(
            quiz_id=quiz_id,
            user_id=user_id
        )
        self._session.add(quiz_user)
        await self._session.commit()
        await self._session.refresh(quiz_user)
        return GeneralResponse.OK

    async def get(self, quiz_id: int, user_id: int) -> QuizUser:
        statement = select(QuizUser).where(QuizUser.quiz_id == quiz_id)\
            .where(QuizUser.user_id == user_id).where(QuizUser.deactivated == False)
        results = await self._session.execute(statement=statement)
        team = results.scalar_one_or_none()  # type: QuizUser | None
        return team

    async def update(self, quiz_user: QuizUser, answer: str) -> Quiz:
        quiz_user.answer = answer
        self._session.add(quiz_user)
        await self._session.commit()
        await self._session.refresh(quiz_user)
        return GeneralResponse.OK
