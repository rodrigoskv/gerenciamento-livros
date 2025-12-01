from sqlalchemy.ext.asyncio import async_object_session, AsyncAttrs
from sqlalchemy.orm import declarative_base


class Base(declarative_base(), AsyncAttrs):
    __abstract__ = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def session(self):
        return async_object_session(self)

    @property
    def a(self) -> AsyncAttrs._AsyncAttrGetitem:
        return self.awaitable_attrs


from .books.book import *
from .users.user import *
