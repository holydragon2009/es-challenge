import random

import requests
from fastapi import HTTPException
from fastapi import APIRouter, Depends

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repo
from app.db.repositories.quiz_repo import QuizRepository

from app.models.domain.user import User
from app.models.schemas.quiz_user import JoinQuizRequest, SubmitAnswerRequest

router = APIRouter()


@router.post("/{quiz_id}/join")
async def join_quiz(
    quiz_id: int,
    quiz_repo: QuizRepository = Depends(get_repo(QuizRepository)),
    user: User = Depends(get_current_user_authorizer()),
):
    return await quiz_repo.create(user.id, quiz_id)


@router.post("/{quiz_id}/answer")
async def submit_answer(
    quiz_id: int,
    request: SubmitAnswerRequest,
    quiz_repo: QuizRepository = Depends(get_repo(QuizRepository)),
    user: User = Depends(get_current_user_authorizer()),
):
    quiz_user = await quiz_repo.get(quiz_id=quiz_id, user_id=user.id)
    if not quiz_user:
        raise HTTPException(status_code=404, detail="Quiz not found")
    res = requests.post(
        url='leaderboard/{quiz_id}/score',
        headers={"Content-Type": "application/json"},
        data={"score": random.randint(1, 100)},
        timeout=10
    )
    res.raise_for_status()  # Check if the response returned a 4xx or 5xx
    print(
        f"POST Response Status: {res.status_code}, Response Body: {res.text}")
    return await quiz_repo.update(
        quiz_user=quiz_user,
        answer=request.answer
    )
