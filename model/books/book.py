# from sqlalchemy import Column, Integer, String, NotNullable, SmallInteger
# from sqlalchemy.dialects.mysql import VARCHAR
# from sqlalchemy import Column, String, Integer, Text
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
#
# class Book(Base):
#     __tablename__ = "books"
#
#     id: Column[int] | int = Column(Integer,primary_key=True, autoincrement=True)
#     title: Column[str] | str = Column(String(25), nullable=False)
#     author: Column[str] | str = Column(String(25),nullable=False)
#     published_year: Column[int] | int = Column(SmallInteger, nullable=True)
#     isbn: Column[str] | str = Column(String(), unique=True)
#
# @classmethod
# def get_all_books:
#     return