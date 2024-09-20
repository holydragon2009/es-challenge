from typing import List, TypeVar, Generic

T = TypeVar('T')


class PaginationResponse(Generic[T]):
    def __init__(self, items: List[T], total: int):
        self.items = items
        self.total = total

    @classmethod
    def of(cls, items: List[T], total: int) -> 'PaginationResponse[T]':
        return cls(items, total)
