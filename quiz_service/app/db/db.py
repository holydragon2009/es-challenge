from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

from sqlalchemy.orm import sessionmaker
from loguru import logger

# DATABASE_URL = os.environ.get("DATABASE_URL")
from app.core.config import DATABASE_URL


engine = AsyncEngine(create_engine(DATABASE_URL, echo=True, future=True))


async def init_db():
    logger.info("Connecting to {0}", repr(DATABASE_URL))
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Connection established")


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
