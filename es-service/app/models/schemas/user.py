from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.common import TimestampModel, SchemaBase
from app.services import security


class UserBase(SchemaBase):
    name: str
    email: str
    avatar: Optional[str] = None


class UserInCreate(UserBase):
    password: str = ""
    pass


class UserInRead(UserBase, TimestampModel):
    id: Optional[int]


class UserWithToken(UserBase):
    token: str


class UserWithHashedPassword(UserBase):
    id: Optional[int]
    salt: Optional[str] = None
    hashed_password: Optional[str] = None

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.hashed_password = security.get_password_hash(self.salt + password)


class UserInResponse(BaseModel):
    user: UserWithToken


class UserInLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: int
    deactivated: bool
    # items: list[Item] = []

    # class Config:
    #     orm_mode = True
