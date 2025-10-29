from http import HTTPStatus
from fastapi import APIRouter
from schema.book.book import BookCreate

router = APIRouter()

@router.post("/books/", status_code= HTTPStatus.CREATED)
def create_book(book: BookCreate):
    breakpoint()
    return book




