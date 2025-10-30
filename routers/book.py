from http import HTTPStatus
from fastapi import APIRouter
from schema.book.book import *

router = APIRouter()

database=[]

@router.post("/books/", status_code= HTTPStatus.CREATED, response_model=BookPublic)
def create_book(book: BookSchema):
    book_with_id=BookId(**book.model_dump(), id=len(database)+1) #** desempacota o dicionario(separa por argumentos e entrega por parametros corretos)
    #da no mesmo escrever um
    #book_with_id=BookId(title=book.title,author=book.author, published_year=book.published_year, isbn=book.isbn, id=len(database)+1)
    database.append(book_with_id)
    return book_with_id

# @router.get("/books/get", status_code=HTTPStatus.ACCEPTED, responses=BookGet)
