from email.message import Message
from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.books.book import Book
from database import get_db
from schema import *

router = APIRouter()

@router.post("/books/", status_code=HTTPStatus.CREATED, response_model=BookPublic)
def create_book(book: BookSchema, session : Session=Depends(get_db())):
    db_book = session(
        select(Book).where(
            (Book.title == book.title) | (Book.author == book.author) | (Book.published_year == book.published_year) | (Book.isbn == book.isbn)
        ))
    if db_book:
        if db_book.title == book.title:
            raise HTTPException(
            status_code = HTTPStatus.CONFLICT,
            detail="O título do livro já existe")
        if db_book.isbn == book.isbn:
            raise HTTPException(
            status_code = HTTPStatus.CONFLICT,
            detail="Esse código já existe")

    db_book = Book(title=book.title, author=book.author, published_year = book.published_year, isbn=book.isbn)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@router.get("/books", response_model=BookList)
def get_all_books(session: Session = Depends(get_db())):
    books = session(select(Book))
    return {"books" : books}

@router.get("/books/{book_id}", response_model=BookPublic)
def get_book_by_id(book_id: int, session : Session=Depends(get_db())):
   db_book = session.scalar(select(Book).where(Book.id == book_id))
   if not db_book:
       raise HTTPException(
           status_code=HTTPStatus.NOT_FOUND,
           detail="ID não encontrado"
       )
   return db_book

@router.put("/books/{book_id}", response_model=BookPublic)
def update_book(book_id: int, book: BookSchema, session : Session=Depends(get_db())):
    db_book = session.scalar(select(Book).where(Book.id == book_id))
    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ID não encontrado"
        )
    db_book.title = book.title
    db_book.author = book.author
    db_book.published_year = book.published_year
    db_book.isbn = book.isbn

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book

@router.delete("/books/{book_id}", response_model=Message)
def delete_book(book_id : int, session : Session=Depends(get_db())):
    db_book = session.scalar(select(Book).where(Book.id == book_id))
    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ID não encontrado"
        )

