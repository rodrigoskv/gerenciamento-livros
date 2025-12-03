from fastapi import FastAPI

from routers.books.book import book
from routers.users.user import user
from routers.auth import auth

app = FastAPI(title="Livros")

app.include_router(user, prefix="/users", tags=['Usuário'])
app.include_router(book, prefix="/books", tags=['Livros'])
app.include_router(auth, prefix="/auth", tags=['Autenticação'])