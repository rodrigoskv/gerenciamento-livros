from database import engine
from model.books.book import Book
from model.users.user import User


def create_tables():
    Book.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)
    print("criou")


if __name__ == "__main__":
    create_tables()
