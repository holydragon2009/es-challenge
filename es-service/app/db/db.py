import typing

from sqlalchemy.ext import asyncio as sa
from sqlalchemy.ext.declarative import declarative_base

from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.orm import sessionmaker
from loguru import logger

# DATABASE_URL = os.environ.get("DATABASE_URL")
from app.core.config import DATABASE_URL


engine = create_async_engine(str(DATABASE_URL), echo=True, future=True)
Base = declarative_base()

# async def create_sa_engine() -> typing.AsyncIterator[sa.AsyncEngine]:
#     logger.debug("Initializing SQLAlchemy engine")
#     engine = sa.create_async_engine(
#         url=str(DATABASE_URL),
#         echo=True,
#         future=True,
#     )
#     logger.debug("SQLAlchemy engine has been initialized")
#     try:
#         yield engine
#     finally:
#         await engine.dispose()
#         logger.debug("SQLAlchemy engine has been cleaned up")

# engine = await create_sa_engine()


async def init_db():
    logger.info("Connecting to {0}", repr(DATABASE_URL))
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Connection established")


async def get_session() -> AsyncSession:
    # async_session = sa.AsyncSession(
    #     engine, class_=AsyncSession, expire_on_commit=False
    # )
    # async with async_session() as session:
    async with sa.AsyncSession(engine, expire_on_commit=False, autoflush=False) as session:
        yield session
