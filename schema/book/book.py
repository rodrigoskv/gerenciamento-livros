from typing import Optional

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
