from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

import model
import schema
from database import get_db

book = APIRouter()


@book.post("/books/", responses={
    409: dict(description="Book already registered"),
}, status_code=HTTPStatus.CREATED)
def create_book(book: schema.BookSchema, session: Session = Depends(get_db)):
    db_book = session.scalar(select(model.Book).where(model.Book.isbn == book.isbn))
    # or_(
    #    (Book.title == book.title),
    #    (Book.author == book.author),
    #    (Book.published_year == book.published_year),
    #    (Book.isbn == book.isbn)
    # )
    # (print(db_book))
    # se for igual = HTTPException
    # se não, db_book = None

    if db_book:
        if db_book.isbn == book.isbn:
            raise HTTPException(status.HTTP_409_CONFLICT, "Book already registered")

    print('m', book)
    db_book = model.Book(title=book.title, author=book.author, published_year=book.published_year, isbn=book.isbn)

    session.add(db_book)
    session.commit()
    session.close()
    return


@book.get("/books", response_model=schema.BookList)
def get_all_books(session: Session = Depends(get_db)):
    books = session.query(model.Book).all()
    session.close()
    return {"books": books}


@book.get("/books/{book_id}", response_model=schema.Book)
def get_book_by_id(book_id: int, session: Session = Depends(get_db)):
    db_book = session.scalar(select(model.Book).where(model.Book.id == book_id))
    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ID não encontrado"
        )
    session.close()
    return db_book


@book.put("/books/{book_id}", response_model=schema.Book)
def update_book(book_id: int, book: schema.BookSchema, session: Session = Depends(get_db)):
    db_book = session.scalar(select(model.Book).where(model.Book.id == book_id))
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
    session.close()

    return db_book


@book.delete("/books/{book_id}", response_model=str)
def delete_book(book_id: int, session: Session = Depends(get_db)):
    db_book = session.scalar(select(model.Book).where(model.Book.id == book_id))
    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ID não encontrado"
        )
    session.delete(db_book)
    session.commit()
    session.close()

    return "Livro deletado"
