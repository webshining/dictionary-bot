from contextlib import asynccontextmanager
from datetime import datetime, timezone

from sqlalchemy import DateTime, and_, select
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from data.config import DB_URI

async_engine = create_async_engine(DB_URI, echo=False, pool_size=20, max_overflow=5, future=True)
async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_session():
    async with async_session() as session:
        yield session


async def get_session_depends():
    async with async_session() as session:
        yield session


def execute(func):
    async def wrapper(*args, **kwargs):
        if not "session" in kwargs:
            async with get_session() as session:
                kwargs["session"] = session
                return await func(*args, **kwargs)

        return await func(*args, **kwargs)

    return wrapper


class Base(AsyncAttrs, DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    created_on: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_on: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
    )

    @classmethod
    async def get(cls, id: int, session: AsyncSession = None):
        stmt = select(cls).where(cls.id == id)
        obj = await session.scalar(stmt)
        return obj

    @classmethod
    @execute
    async def get_all(cls, session: AsyncSession = None):
        stmt = select(cls)
        objs = (await session.scalars(stmt)).all()
        return objs

    @classmethod
    @execute
    async def get_by(cls, session: AsyncSession = None, **kwargs):
        stmt = select(cls).where(and_(getattr(cls, k) == v for k, v in kwargs.items()))
        obj = await session.scalar(stmt)
        return obj

    @classmethod
    @execute
    async def create(cls, session: AsyncSession = None, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        await session.flush()
        await session.commit()
        return obj

    @classmethod
    @execute
    async def update(cls, id: int, session: AsyncSession = None, **kwargs):
        if obj := await cls.get(id, session=session):
            for key, value in kwargs.items():
                setattr(obj, key, value)
            await session.flush()
            await session.commit()
        return obj

    @classmethod
    @execute
    async def delete(cls, id: int, session: AsyncSession = None):
        if obj := await cls.get(id, session=session):
            await session.delete(obj)
            await session.flush()
            await session.commit()

    @classmethod
    @execute
    async def delete_by(cls, session: AsyncSession = None, **kwargs):
        if obj := await cls.get_by(session=session, **kwargs):
            await session.delete(obj)
            await session.flush()
            await session.commit()

    @classmethod
    @execute
    async def get_or_create(cls, id: str | int, session: AsyncSession = None, **kwargs):
        if obj := await cls.get(id, session=session):
            return obj
        return await cls.create(id=id, session=session, **kwargs)

    @classmethod
    @execute
    async def update_or_create(cls, id: str | int, session: AsyncSession = None, **kwargs):
        if user := await cls.update(id=id, session=session, **kwargs):
            return user
        return await cls.create(id=id, session=session, **kwargs)
