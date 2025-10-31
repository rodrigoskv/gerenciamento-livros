from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from schema.book.book import *

router = APIRouter()

database = []

@router.post("/books/", status_code=HTTPStatus.CREATED, response_model=BookPublic)
def create_book(book: BookSchema):
    book_with_id = BookId(**book.model_dump(), id=len(
        database) + 1)  # ** desempacota o dicionario(separa por argumentos e entrega por parametros corretos)
    # da no mesmo escrever um
    # book_with_id=BookId(title=book.title,author=book.author, published_year=book.published_year, isbn=book.isbn, id=len(database)+1)
    database.append(book_with_id)
    return book_with_id

@router.get("/books", response_model=BookList)
def get_all_books():
    return {"books" : database}

@router.get("/books/{book_id}", response_model=BookPublic)
def get_book_by_id(book_id: int):
    if book_id > len(database) or book_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    book_with_id = database[book_id -1]
    return book_with_id

@router.put("/books/{book_id}", response_model=BookPublic)
def update_book(book_id: int, book: BookSchema):
    if book_id > len(database) or book_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    book_with_id = BookId(**book.model_dump(), id = book_id)
    database[book_id-1] = book_with_id
    return book_with_id

@router.delete("/books/{book_id}", response_model=str)
def delete_book(book_id : int):
    if book_id > len(database) or book_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail= "User not found"
        )
    del database[book_id -1]
    return "Livro excluído"
