from fastapi import APIRouter

from app.api.routes import teams, authentication, users, organizations, datasets
from app.core.config import API_VERSION


router = APIRouter()

# router.include_router(token.router, tags=["token"])
router.include_router(authentication.router, tags=["authentication"], prefix=API_VERSION + "/authentication")
router.include_router(teams.router, tags=["quiz"], prefix=API_VERSION + "/quiz")
router.include_router(users.router, tags=["leaderboard"], prefix=API_VERSION + "/leaderboard")

