from fastapi import HTTPException
from fastapi import status as http_status
from sqlmodel import select

import app.models.schemas.user
from app.db.errors import EntityDoesNotExist
from app.db.repositories.base_repo import BaseRepo
from app.models.domain.user import User
from app.services import security

schema = app.models.schemas.user


class UserRepository(BaseRepo):

    async def create(self, data: schema.UserInCreate) -> User:
        # add new user
        salt = security.generate_salt()
        hashed_password = security.get_password_hash(salt + data.password)
        user = User(name=data.name, email=data.email, avatar=data.avatar,
                    salt=salt, hashed_password=hashed_password)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return schema.User(
            id=user.id,
            email=user.email,
            name=user.name,
            deactivated=user.deactivated,
            salt=user.salt,
            hashed_password=user.hashed_password
        )

    async def get(self, user_id: int) -> schema.User:
        results = await self._session.execute(select(User).where(User.id == user_id).where(User.deactivated == False))
        user = results.scalar_one_or_none()  # type: User | None
        if user is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Not found this user"
            )
        return schema.User(
            id=user.id,
            email=user.email,
            name=user.name,
            deactivated=user.deactivated,
            salt=user.salt,
            hashed_password=user.hashed_password
        )

    async def get_user_by_email(self, *, email: str) -> schema.UserWithHashedPassword:
        results = await self._session.execute(select(User).where(User.email == email).where(User.deactivated == False))
        user = results.scalar_one_or_none()  # type: User | None
        if user:
            return schema.UserWithHashedPassword(
                id=user.id,
                email=user.email,
                name=user.name,
                deactivated=user.deactivated,
                salt=user.salt,
                hashed_password=user.hashed_password
            )
        raise EntityDoesNotExist("user with email {0} does not exist".format(email))

