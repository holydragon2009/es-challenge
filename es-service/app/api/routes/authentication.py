import json

import requests
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from app.api.dependencies.database import get_repo
from app.core import config
from app.db.errors import EntityDoesNotExist
from app.db.repositories.user_repository import UserRepository
from app.models.schemas.google_authen import GoogleAuthen
from app.models.schemas.user import UserInCreate, UserInResponse, UserWithToken, UserInLogin
from app.resources import strings
from app.services import jwt
from app.services.authentication import check_email_is_taken

router = APIRouter()


@router.post("/google-login")
async def google_login(
    *,
    google_authen: GoogleAuthen = Body(..., embed=True),
    user_repo: UserRepository = Depends(get_repo(UserRepository)),
):
    wrong_login_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="Incorrect Google authentication")
    if not google_authen.token:
        raise wrong_login_error
    access_token_uri = (
        "https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=" + google_authen.token
    )
    try:
        response = requests.get(url=access_token_uri)
        profile = json.loads(response.text)
        username = profile["email"]
    except KeyError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid token")
    try:
        user = await user_repo.get_user_by_email(email=google_authen.email)
    except EntityDoesNotExist as existence_error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User with this email does not exist")
    token = jwt.create_access_token_for_user(user, str(config.SECRET_KEY))
    return UserInResponse(
        user=UserWithToken(
            email=user.email,
            name=user.name,
            avatar=user.avatar,
            token=token,
        ),
    )


@router.post("/login", response_model=UserInResponse, name="auth:login")
async def login(
    user_login: UserInLogin = Body(..., embed=False),
    user_repo: UserRepository = Depends(get_repo(UserRepository)),
) -> UserInResponse:
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=strings.INCORRECT_LOGIN_INPUT,
    )

    try:
        user = await user_repo.get_user_by_email(email=user_login.email)
    except EntityDoesNotExist as existence_error:
        raise wrong_login_error from existence_error

    if not user.check_password(user_login.password):
        raise wrong_login_error

    token = jwt.create_access_token_for_user(user, str(config.SECRET_KEY))
    return UserInResponse(
        user=UserWithToken(
            email=user.email,
            name=user.name,
            avatar=user.avatar,
            token=token,
        ),
    )


@router.post(
    "/register",
    status_code=HTTP_201_CREATED,
    response_model=UserInResponse,
    name="auth:register",
)
async def register(
    user_create: UserInCreate = Body(..., embed=True, alias="user"),
    user_repo: UserRepository = Depends(get_repo(UserRepository)),
) -> UserInResponse:
    if await check_email_is_taken(user_repo, user_create.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.EMAIL_TAKEN,
        )

    user = await user_repo.create(user_create)

    token = jwt.create_access_token_for_user(user, str(config.SECRET_KEY))
    return UserInResponse(
        user=UserWithToken(
            email=user.email,
            name=user.name,
            avatar=user.avatar,
            token=token,
        ),
    )
