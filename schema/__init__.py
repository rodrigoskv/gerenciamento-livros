import pydantic
class BaseModel(pydantic.BaseModel):
    @classmethod
    async def from_orm_async(cls, *args, **kwargs):
        o = None
        if len(args) > 0:
            o = args[0]
        if o is None and len(kwargs) == 0:
            return None
        kwargs_keys = kwargs.keys()
        data = {
            **({} if o is None else {
                field: await cls.__parse_value_async(field, o, await cls.__get_attr_async(o, field))
                for field in cls.fields()
                if field not in kwargs_keys}),
            **{
                field: await cls.__parse_value_async(field, o, value)
                for field, value in kwargs.items()},
        }
        return cls(**data)

from .book.book import *