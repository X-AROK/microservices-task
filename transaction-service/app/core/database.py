from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class Database:
    def __init__(self, db_url: str) -> None:
        self.__engine = create_async_engine(db_url)
        self.__sessionmaker = async_sessionmaker(bind=self.__engine)

    @asynccontextmanager
    async def session(self):
        session = self.__sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
