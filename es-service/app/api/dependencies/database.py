from typing import Callable, Type
from fastapi import Depends
from app.db.db import get_session
from app.db.repositories.base_repo import BaseRepo

from sqlalchemy.orm import Session


def get_repo(
    repo_type: Type[BaseRepo],
) -> Callable[[Session], BaseRepo]:
    def _get_rep(
        session: Session = Depends(get_session),
    ) -> BaseRepo:
        return repo_type(session)

    return _get_rep

