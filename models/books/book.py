from sqlalchemy import SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    published_year: Mapped[int] = mapped_column(SmallInteger)
    isbn: Mapped[str] = mapped_column(unique=True, nullable=False)

