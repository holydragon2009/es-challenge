from typing import List, Optional

from fastapi import HTTPException
from fastapi import status as http_status
from sqlmodel import select, or_, col, join
from sqlalchemy import func
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.errors import EntityDoesNotExist
from app.db.repositories.base_repo import BaseRepo
from app.models.domain.team import Team
from app.models.domain.team_dataset import TeamDataset
from app.models.domain.user import UserInCreate, User, UserWithTeam, UserBase, UserInRead
from app.models.domain.user_dataset import UserDataset, UserDatasetRestrictionInUpdate
from app.models.domain.user_team_link import UserTeamLink
from app.resources import strings
from app.services.dynamodb import delete_dataset, add_dataset, update_dataset_restrictions, add_user, delete_user


class UserRepository(BaseRepo):

    async def create(self, data: UserInCreate) -> User:
        if add_user(data.email, data.organization_id):
            # add new user
            user = User(name=data.name, email=data.email, avatar=data.avatar, organization_id=data.organization_id)
            self._session.add(user)
            await self._session.commit()
            await self._session.refresh(user)
            return user

    async def get(self, user_id: int) -> User:
        statement = select(User).where(User.id == user_id).where(User.deactivated == False)
        results = await self._session.execute(statement=statement)
        user = results.scalar_one_or_none()  # type: User | None
        if user is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Not found this user"
            )
        return user


    async def get_user_by_email(self, *, email: str) -> User:
        results = await self._session.execute(select(User).where(User.email == email).where(User.deactivated == False))
        res = results.scalar_one_or_none()  # type: UserDataset | None
        if res:
            return User(name=res.name, email=res.email, avatar=res.avatar, id=res.id)
        raise EntityDoesNotExist("user with email {0} does not exist".format(email))

