from fastapi import APIRouter

from app.api.routes import authentication
from app.api.routes import quiz
from app.api.routes import leaderboard
from app.core.config import API_VERSION


router = APIRouter()

# router.include_router(token.router, tags=["token"])
router.include_router(authentication.router, tags=["authentication"], prefix=API_VERSION + "/authentication")
router.include_router(quiz.router, tags=["quiz"], prefix=API_VERSION + "/quiz")
router.include_router(leaderboard.router, tags=["leaderboard"], prefix=API_VERSION + "/leaderboard")

