from typing import Callable, Optional

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from starlette import requests, status
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.dependencies.database import get_repo
from app.core.config import JWT_TOKEN_PREFIX, SECRET_KEY
from app.db.errors import EntityDoesNotExist
from app.db.repositories.user_repository import UserRepository
from app.models.domain.user import User
from app.resources import strings
from app.services import jwt

HEADER_KEY = "Authorization"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class RWAPIKeyHeader(APIKeyHeader):
    async def __call__(  # noqa: WPS610
        self,
        request: requests.Request,
    ) -> Optional[str]:
        try:
            return await super().__call__(request)
        except StarletteHTTPException as original_auth_exc:
            raise HTTPException(
                status_code=original_auth_exc.status_code,
                detail=strings.AUTHENTICATION_REQUIRED,
            )


def get_current_user_authorizer(*, required: bool = True) -> Callable:  # type: ignore
    return _get_current_user if required else _get_current_user_optional


def _get_authorization_header_retriever(
    *,
    required: bool = True,
) -> Callable:  # type: ignore
    return _get_authorization_header if required else _get_authorization_header_optional


def _get_authorization_header(
    api_key: str = Security(RWAPIKeyHeader(name=HEADER_KEY)),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )

    if token_prefix != JWT_TOKEN_PREFIX:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )

    return token


def _get_authorization_header_optional(
    authorization: Optional[str] = Security(
        RWAPIKeyHeader(name=HEADER_KEY, auto_error=False),
    ),
) -> str:
    if authorization:
        return _get_authorization_header(authorization)

    return ""


def _get_authorization_token(authorization: str = Depends(oauth2_scheme)):
    return authorization


async def _get_current_user(
    user_repo: UserRepository = Depends(get_repo(UserRepository)),
    # token: str = Depends(_get_authorization_header_retriever()),
    token: str = Depends(_get_authorization_token),
) -> User:
    try:
        email = jwt.get_username_from_email(token, str(SECRET_KEY))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )

    try:
        return await user_repo.get_user_by_email(email=email)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )


async def _get_current_user_optional(
    user_repo: UserRepository = Depends(get_repo(UserRepository)),
    # token: str = Depends(_get_authorization_header_retriever(required=False)),
    token: str = Depends(_get_authorization_token),
) -> Optional[User]:
    if token:
        return await _get_current_user(user_repo, token)

    return None


