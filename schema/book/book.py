from typing import Optional
from pydantic import Field

from schema import BaseModel


class BookSchema(BaseModel):
    title: str
    author: str
    published_year: int
    isbn: str


class Book(BookSchema):
    id: int


class BookList(BaseModel):
    books: list[Book]


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    published_year: Optional[int] = None
    isbn: Optional[str] = None

class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)