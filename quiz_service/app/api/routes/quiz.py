from fastapi import HTTPException
from fastapi import APIRouter, Depends

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repo
from app.db.repositories.quiz_repo import QuizRepository

from app.models.domain.quiz import JoinQuizRequest, SubmitAnswerRequest
from app.models.domain.user import User


router = APIRouter()


@router.post("/quiz/{quiz_id}/join")
async def join_quiz(
    quiz_id: int,
    request: JoinQuizRequest,
    quiz_repo: QuizRepository = Depends(get_repo(QuizRepository)),
    user: User = Depends(get_current_user_authorizer()),
):
    request.user_id = user.id
    request.quiz_id = quiz_id
    return await quiz_repo.create(request)


@router.post("/quiz/{quiz_id}/answers")
async def submit_answer(
    quiz_id: int,
    request: SubmitAnswerRequest,
    quiz_repo: QuizRepository = Depends(get_repo(QuizRepository)),
    user: User = Depends(get_current_user_authorizer()),
):
    quiz = await quiz_repo.get(quiz_id=quiz_id, user_id=user.id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return await quiz_repo.update(
        user_id=user.id,
        quiz_id=quiz_id,
        answers=request.answers)

