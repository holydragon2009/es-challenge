from app.core.general import GeneralResponse
from app.db.repositories.base_repo import BaseRepo
from app.models.domain.leaderboard import Leaderboard
from app.models.schemas.leaderboard import UpdateScoreRequest


class LeaderboardRepository(BaseRepo):

    async def create(self, data: UpdateScoreRequest, quiz_id: int, user_id: int) -> Leaderboard:
        leaderboard = Leaderboard(
            quiz_id=quiz_id,
            user_id=user_id,
            score=data.score
        )
        self._session.add(leaderboard)
        await self._session.commit()
        await self._session.refresh(leaderboard)
        return GeneralResponse.OK

