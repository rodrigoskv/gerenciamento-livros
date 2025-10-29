from fastapi import FastAPI
from routers.book import router

app = FastAPI(title="Libros")
app.include_router(router)