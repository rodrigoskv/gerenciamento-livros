from sqlalchemy import SmallInteger, Column, Integer, ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base


class Book(Base):
    __tablename__ = "Book"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    published_year: Mapped[int] = mapped_column(SmallInteger)
    isbn: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    user_id : Mapped[int] = Column(Integer, ForeignKey("User.id"))

    user = relationship("User", back_populates="books")
