from typing import AsyncGenerator

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from jjnt_api.consts import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

_sqlalchemy_db_uri = URL.create(
    drivername="postgresql+psycopg_async",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

_engine = create_async_engine(_sqlalchemy_db_uri)

LocalAsyncSession = sessionmaker(  # type: ignore
    bind=_engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

BaseModel = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with LocalAsyncSession() as session:
        yield session
