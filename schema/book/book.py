from typing import Optional
import model
from schema import BaseModel

class BookSchema(BaseModel):
    title : str
    author : str
    published_year : int
    isbn : str

class BookPublic(BaseModel):
    id : int
    title: str
    author: str
    published_year: int
    isbn: str

class BookId(BookSchema):
    id:int

class BookList(BaseModel):
    books: list[BookPublic]

class BookUpdate(BaseModel):
    title : Optional[str] = None
    author : Optional [str] = None
    published_year : Optional[int]= None
