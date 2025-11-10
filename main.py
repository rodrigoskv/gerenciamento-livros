from fastapi import FastAPI
from routers.books.book import book
from routers.users.user import user

app = FastAPI(title="Libros")
app.include_router(book)
app.include_router(user)