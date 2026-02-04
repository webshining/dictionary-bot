from contextlib import asynccontextmanager
from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, class_mapper

from data.config import DB_URI

async_engine = create_async_engine(DB_URI)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


@asynccontextmanager
async def get_session():
    async with async_session() as session:
        yield session


async def get_session_generator():
    async with async_session() as session:
        yield session


def execute(func):
    async def wrapper(*args, **kwargs):
        if "session" not in kwargs:
            async with get_session() as session:
                kwargs["session"] = session
                return await func(*args, **kwargs)

        return await func(*args, **kwargs)

    return wrapper


class Base(AsyncAttrs, DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

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
    async def get_by(cls, *args, session: AsyncSession = None):
        stmt = select(cls).where(and_(*args))
        obj = await session.scalar(stmt)
        return obj

    @classmethod
    @execute
    async def create(cls, session: AsyncSession = None, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    @execute
    async def update(cls, id: int, session: AsyncSession = None, **kwargs):
        async with session.begin():
            if obj := await cls.get(id, session=session):
                for key, value in kwargs.items():
                    setattr(obj, key, value)
                await session.flush()
        return obj

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

    def to_dict(self):
        state = self.__getstate__()
        if "_sa_instance_state" in state:
            del state["_sa_instance_state"]

        columns = state.keys()
        state = dict(map(self.__get_key_value, columns))

        return state

    def __get_key_value(self, c):
        attr = getattr(self, c)
        return (
            (c, attr.isoformat())
            if isinstance(attr, datetime)
            else (
                (c, attr.to_dict())
                if isinstance(attr, BaseModel)
                else (
                    (c, [i.to_dict() for i in attr])
                    if isinstance(attr, list) and len(attr) > 0 and isinstance(attr[0], BaseModel)
                    else (c, attr)
                )
            )
        )
