from typing import Optional, List
from pydantic import Field

from schema import BaseModel


class BookSchema(BaseModel):
    title: str
    author: str
    published_year: int
    isbn: str


class Book(BookSchema):
    id: int
    user_id: Optional[int] = None


class BookList(BaseModel):
    books: List[Book]


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    published_year: Optional[int] = None
    isbn: Optional[str] = None

class FilterPage(BaseModel):
    offset: Optional[int] = None
    limit: Optional[int] = None