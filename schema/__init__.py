import inspect
import os
import typing
import pydantic
from sqlalchemy.orm import Query


class CachedSyncCall:
    is_production = os.environ.get('ENV') != 'production'

    def __init__(self, function: typing.Callable):
        self.cache = {}
        self.function = function

    def __call__(self, *args):
        if self.is_production:
            return self.function(*args)
        value = self.cache.get(args)
        if value is None:
            value = self.cache[args] = self.function(*args)
        return value


_typing_get_type_hints = CachedSyncCall(typing.get_type_hints)
_typing_get_origin = CachedSyncCall(typing.get_origin)
_typing_get_args = CachedSyncCall(typing.get_args)
_inspect_isclass = CachedSyncCall(inspect.isclass)
_issubclass = CachedSyncCall(issubclass)


class BaseModel(pydantic.BaseModel):

    @classmethod
    def fields(cls):
        return getattr(cls, 'model_fields', cls.model_fields)

    def extract_data_to(self, data, ignore: list = None):
        if ignore is None:
            ignore = []
        for field in self.fields():
            if field not in ignore:
                data.__setattr__(field, self.__getattribute__(field))

    def to_dict(self):
        return self.model_dump(mode='json')

    def to_json(self):
        return self.model_dump_json()

    @staticmethod
    def __is_convertible(field_type, value) -> bool:
        return (
                _inspect_isclass(field_type) and
                _inspect_isclass(type(value)) and
                _issubclass(field_type, BaseModel) and
                not isinstance(value, BaseModel)
        )

    @classmethod
    def __parse_final_value(cls, field_type, value):
        try:
            if cls.__is_convertible(field_type, value):
                return field_type.from_orm(value)

            if _typing_get_origin(field_type) is list:
                return cls.__parse_list(field_type, value)

            if field_type is dict:
                return dict(value)

            if _typing_get_origin(field_type) is typing.Union:
                for union_field_type in _typing_get_args(field_type):

                    if cls.__is_convertible(union_field_type, value):
                        return union_field_type.from_orm(value)

                    if _typing_get_origin(union_field_type) is list:
                        return cls.__parse_list(union_field_type, value)

                    if union_field_type is dict:
                        return dict(value)
        except Exception as e:
            print(f"SCHEMA Error Converting {value} to {field_type}")
            raise e

        return value

    @classmethod
    def __parse_list(cls, field_type, value):
        item_type = _typing_get_args(field_type)[0]
        return [
            cls.__parse_final_value(item_type, item)
            for item in value
        ]

    @classmethod
    def __parse_value(cls, field, value):
        if value is None:
            return None
        field_type = _typing_get_type_hints(cls)[field]
        return cls.__parse_final_value(field_type, value)

    @classmethod
    def from_orm(cls, *args, **kwargs):
        o = None
        if len(args) > 0:
            o = args[0]
        if o is None and len(kwargs) == 0:
            return None
        kwargs_keys = kwargs.keys()
        data = {
            **({} if o is None else {
                field: cls.__parse_value(field, getattr(o, field))
                for field in cls.fields()
                if field not in kwargs_keys and hasattr(o, field)
            }),
            **{
                field: cls.__parse_value(field, value)
                for field, value in kwargs.items()
            },
        }
        return cls(**data)

    @classmethod
    async def __parse_final_value_async(cls, field_type, obj, value):
        try:
            if inspect.isawaitable(value):
                value = await value
                if value is None:
                    return None

            if cls.__is_convertible(field_type, value):
                return await field_type.from_orm_async(value)

            if _typing_get_origin(field_type) is list:
                return await cls.__parse_list_async(field_type, obj, value)

            if field_type is dict:
                return dict(value)

            if _typing_get_origin(field_type) is typing.Union:
                for union_field_type in _typing_get_args(field_type):

                    if cls.__is_convertible(union_field_type, value):
                        return await union_field_type.from_orm_async(value)

                    if _typing_get_origin(union_field_type) is list:
                        return await cls.__parse_list_async(union_field_type, obj, value)

                    if union_field_type is dict:
                        return dict(value)

        except Exception as e:
            print(f"SCHEMA Error Converting to field_type={field_type}; obj={obj}; value={value};")
            raise e

        return value

    @classmethod
    async def __parse_list_async(cls, field_type, obj, value):
        item_type = _typing_get_args(field_type)[0]

        if isinstance(value, Query) and obj is not None:
            return [
                await cls.__parse_final_value_async(item_type, obj, item)
                for item in await obj.session.scalars(value)
            ]

        return [
            await cls.__parse_final_value_async(item_type, obj, item)
            for item in value
        ]

    @classmethod
    async def __parse_value_async(cls, field, obj, value):
        try:
            if value is None:
                return None
            field_type = _typing_get_type_hints(cls)[field]
            return await cls.__parse_final_value_async(field_type, obj, value)
        except Exception as e:
            print(f"Schema conversion error field={field}; obj={obj}; value={value}; exception={e}")
            raise e

    @classmethod
    async def __get_attr_async(cls, o, field):
        if _inspect_isclass(type(o)):
            awaitable = getattr(o, 'awaitable_attrs', None)
            if awaitable is not None:
                return getattr(awaitable, field, None)
        return getattr(o, field, None)

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
                if field not in kwargs_keys
            }),
            **{
                field: await cls.__parse_value_async(field, o, value)
                for field, value in kwargs.items()
            },
        }
        return cls(**data)



from .book.book import *
from .user.user import *
