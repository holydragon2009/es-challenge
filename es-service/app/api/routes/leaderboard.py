import random
from fastapi import APIRouter, Depends

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repo
from app.db.repositories.leaderboard_repo import LeaderboardRepository
from app.models.domain.user import User
from app.models.schemas.leaderboard import UpdateScoreRequest

router = APIRouter()


@router.post("/{quiz_id}/score")
async def update_score(
    quiz_id: int,
    request: UpdateScoreRequest,
    leaderboard_repo: LeaderboardRepository = Depends(get_repo(LeaderboardRepository)),
    user: User = Depends(get_current_user_authorizer()),
):
    return await leaderboard_repo.create(request, quiz_id, user.id)




