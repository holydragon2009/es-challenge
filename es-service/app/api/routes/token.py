from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.api.dependencies.database import get_repo
from app.db.repositories.user_repository import UserRepository
from app.services.token_utils import create_access_token
from app.db.errors import EntityDoesNotExist
from app.models.domain.token import Token
from app.services.jwt import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepository = Depends(get_repo(UserRepository)),
):
    wrong_login_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    try:
        user = await user_repo.get_user_by_email(email=form_data.username)
    except EntityDoesNotExist:
        raise wrong_login_error

    if not user.check_password(form_data.password):
        raise wrong_login_error

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


