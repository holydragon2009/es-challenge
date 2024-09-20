from pydantic import EmailStr, BaseModel
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from app.models.common import TimestampModel, DeactivatedModel
from app.models.domain.quiz import Quiz
from app.services import security


class CredentialModel(SQLModel):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.hashed_password = security.get_password_hash(self.salt + password)


class UserBase(SQLModel):
    name: str
    email: str
    avatar: Optional[str] = None


class User(
    UserBase,
    TimestampModel,
    CredentialModel,
    DeactivatedModel,
    table=True
):
    __tablename__ = 'user'
    id: int = Field(default=None, nullable=False, primary_key=True)
    quizzes: List[Quiz] = Relationship(back_populates="user")


class UserInRead(UserBase, TimestampModel):
    id: Optional[int]


class UserWithToken(UserBase):
    token: str


class UserInResponse(SQLModel):
    user: UserWithToken


class UserInLogin(SQLModel):
    email: EmailStr
    password: str



