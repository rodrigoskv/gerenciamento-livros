from typing import Optional
from schema import BaseModel

class BookSchema(BaseModel):
    id: int
    title : str
    author : str
    published_year : int
    isbn : str

class BookList(BaseModel):
    books: list[BookSchema]

class BookUpdate(BaseModel):
    title : Optional[str] = None
    author : Optional [str] = None
    published_year : Optional[int]= None
    isbn : Optional[str]= None