from typing import List, Optional

from sqlmodel import select, or_, col, Session

from app.db.repositories.base_repo import BaseRepo
from app.models.domain.leaderboard import Leaderboard, UpdateScoreRequest


class LeaderboardRepository(BaseRepo):

    async def create(self, data: UpdateScoreRequest) -> Leaderboard:
        leaderboard = Leaderboard(
            quiz_id=data.quiz_id,
            user_id=data.user_id,
            score=data.score
        )
        self._session.add(leaderboard)
        await self._session.commit()
        await self._session.refresh(leaderboard)
        return leaderboard

