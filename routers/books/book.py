
from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from fastapi.params import Depends
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import model
import schema
from database import get_db

book = APIRouter()
FilterPage = Annotated[schema.FilterPage, Query()]


@book.post("/", responses={
    409: dict(description="Book already registered"),
}, status_code=HTTPStatus.CREATED)
async def create_book(book: schema.BookSchema, session: AsyncSession = Depends(get_db)):
    db_book = await session.scalar(select(model.Book).where(model.Book.isbn == book.isbn))

    if db_book:
        if db_book.isbn == book.isbn:
            raise HTTPException(status.HTTP_409_CONFLICT, "Book already registered")

    print('m', book)
    db_book = model.Book(title=book.title, author=book.author, published_year=book.published_year, isbn=book.isbn)

    session.add(db_book)
    await session.commit()
    await session.close()
    return db_book


@book.get("/", response_model=schema.BookList)
async def get_books(filter_books : FilterPage, session: AsyncSession = Depends(get_db)):
    try:
        books = (select(model.Book))

        if filter_books.offset:
            books.offset(filter_books.offset).limit(filter_books.limit)

        books = await session.scalars(books)
        return await schema.BookList.from_orm_async(books=books)

    finally:
        await session.close()


@book.get("/{book_id}", response_model=schema.Book)
async def get_book_by_id(book_id: int, session: AsyncSession = Depends(get_db)):
    db_book = await session.scalar(select(model.Book).where(model.Book.id == book_id))
    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ID não encontrado"
        )
    await session.close()
    return db_book


@book.put("/{book_id}", response_model=schema.Book)
async def update_book(book_id: int, book: schema.BookSchema, session: AsyncSession = Depends(get_db)):
    db_book = await session.scalar(select(model.Book).where(model.Book.id == book_id))
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
    await session.commit()
    await session.refresh(db_book)
    await session.close()

    return db_book


@book.delete("/{book_id}", response_model=str)
async def delete_book(book_id: int, session: AsyncSession = Depends(get_db)):
    db_book = await session.scalar(select(model.Book).where(model.Book.id == book_id))
    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ID não encontrado"
        )
    await session.delete(db_book)
    await session.commit()
    await session.close()

    return "Livro deletado"
