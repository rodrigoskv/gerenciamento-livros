from sqlalchemy import SmallInteger, Column
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = Column(primary_key=True, autoincrement=True)
    title: Mapped[str] = Column(nullable=False)
    author: Mapped[str] = Column(nullable=False)
    published_year: Mapped[int] = Column(SmallInteger)
    isbn: Mapped[str] = Column(unique=True, nullable=False)

