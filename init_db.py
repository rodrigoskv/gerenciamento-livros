from database import engine
from models.books.book import Book

def create_tables():
    Book.metadata.create_all(bind=engine)
    print("criou")

if __name__ == "__main__":
    create_tables()