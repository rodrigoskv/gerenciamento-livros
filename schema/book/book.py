from typing import Optional
import model
from schema import BaseModel

class BookCreate(BaseModel):
    id : int
    title : str
    autor : str
    published_year : str
    isbn : str