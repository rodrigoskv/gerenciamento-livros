from typing import Optional
import model
from schema import BaseModel

class BookCreate(BaseModel):
    id : int
    title : str
    author : str
    published_year : str
    isbn : str

class BookUpdate(BaseModel):
    title : Optional[str] = None
    author : Optional [str] = None
    published_year : Optional[str]= None

class BookGet(BaseModel):
    id : int
    title : str
    author : str
