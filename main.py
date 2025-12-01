from fastapi import FastAPI

from routers.books.book import book
from routers.users.user import user

app = FastAPI(title="Livros")

app.include_router(user, tags=['Usuário'])
app.include_router(book, tags=['Livros'])
