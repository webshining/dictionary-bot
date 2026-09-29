from contextvars import ContextVar

from pydantic import BaseModel, field_serializer
from surrealdb import AsyncSurreal, AsyncWsSurrealConnection, RecordID

from data.config import (
    SURREAL_DATABASE,
    SURREAL_NAMESPACE,
    SURREAL_PASSWORD,
    SURREAL_URL,
    SURREAL_USERNAME,
)

current_session: ContextVar[AsyncWsSurrealConnection] = ContextVar("current_session")


class DBContext:
    db: AsyncWsSurrealConnection

    def __init__(self):
        self.db = AsyncSurreal(SURREAL_URL)
        self.token = current_session.set(self.db)

    async def connect(self):
        await self.db.connect()
        await self.db.use(SURREAL_NAMESPACE, SURREAL_DATABASE)
        await self.db.signin({"username": SURREAL_USERNAME, "password": SURREAL_PASSWORD})

    async def disconnect(self):
        current_session.reset(self.token)
        await self.db.close()


database = DBContext()


class AwaitableAttrs:
    def __init__(self, instance):
        self.instance = instance

    def __getattr__(self, name):
        async def loader():
            return await self.instance._load_relation(name)

        return loader()


class Base(BaseModel):
    id: RecordID

    @property
    def awaitable_attrs(self):
        return AwaitableAttrs(self)

    @field_serializer("*")
    def serialize_record_ids(self, value):
        if isinstance(value, RecordID):
            return value.id

        return value
