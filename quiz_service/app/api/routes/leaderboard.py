import random
from fastapi import APIRouter, Depends

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repo
from app.db.repositories.leaderboard_repo import LeaderboardRepository
from app.models.domain.leaderboard import UpdateScoreRequest
from app.models.domain.user import User


router = APIRouter()


@router.post("/leaderboard/{quiz_id}/score")
async def update_score(
    quiz_id: int,
    leaderboard_repo: LeaderboardRepository = Depends(get_repo(LeaderboardRepository)),
    user: User = Depends(get_current_user_authorizer()),
):
    request= UpdateScoreRequest(
        user_id=user.id,
        quiz_id=quiz_id,
        score=random.randint(1, 100)
    )

    return await leaderboard_repo.create(request)




