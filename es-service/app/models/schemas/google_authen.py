from pydantic import BaseModel


class GoogleAuthen(BaseModel):
    token: str
    email: str
