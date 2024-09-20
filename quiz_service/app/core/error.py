from typing import Optional

from app.core.general import GeneralResponse


class BaseError:
    def __init__(self, code: int, message: str, detail: Optional[object]):
        self.errorCode = code
        self.message = message
        self.detail = detail

    @classmethod
    def fail(cls):
        return cls(404, GeneralResponse.FAILED, None)


