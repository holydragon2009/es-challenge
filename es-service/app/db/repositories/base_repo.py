from sqlmodel.ext.asyncio.session import AsyncSession


class BaseRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def connection(self) -> AsyncSession:
        return self._session
