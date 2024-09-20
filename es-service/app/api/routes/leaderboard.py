import random
from fastapi import APIRouter, Depends

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repo
from app.db.repositories.leaderboard_repo import LeaderboardRepository
from app.main import sio
from app.models.domain.user import User
from app.models.schemas.leaderboard import UpdateScoreRequest
from app.services.redis import cache

router = APIRouter()


@router.post("/{quiz_id}/score")
async def update_score(
    quiz_id: int,
    request: UpdateScoreRequest,
    leaderboard_repo: LeaderboardRepository = Depends(get_repo(LeaderboardRepository)),
    user: User = Depends(get_current_user_authorizer()),
):
    redis_client: cache = Depends(cache)
    user_sid = redis_client.hget("ws_type", quiz_id, user.id)
    redis_client.hset("leaderboard_type", quiz_id, user.id, user_sid)
    # emit get_user_score event to ws to send user's score to client apps
    await sio.emit(
        to=user_sid,
        data={
            "event_type": "get_user_score",
            "user_id": user.id,
            "quiz_id": quiz_id,
            "user_score": request.score
        }
    )
    # emit get_quiz_leaderboard event to ws to send leaderboard of the quiz to client apps
    await sio.emit(
        to=user_sid,
        data={
            "event_type": "get_quiz_leaderboard",
            "user_id": user.id,
            "quiz_id": quiz_id
        }
    )
    return await leaderboard_repo.create(request, quiz_id, user.id)


