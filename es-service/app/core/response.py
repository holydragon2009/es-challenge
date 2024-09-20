from typing import List, TypeVar, Generic, Optional

from app.core.error import BaseError

T = TypeVar('T')


class BaseResponse(Generic[T]):
    def __init__(self, data: [T]):
        self.data = data


class ApiResponse(BaseResponse):
    def __init__(self, data: [T], is_success: bool, error=Optional[BaseError]):
        super().__init__(data)
        self.is_success = is_success
        self.error = error

    @classmethod
    def of(cls, data: [T]):
        return cls(data, True)

    @classmethod
    def error(cls, error):
        return cls(None, False, error)

    @classmethod
    def ok(cls):
        return cls(None, True)
