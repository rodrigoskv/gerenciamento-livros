import asyncio

from database import *
from model.books.book import Book
from model.users.user import User


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) #dessa forma engloba todos os Base
        print("criou")


if __name__ == "__main__":
    asyncio.run(create_tables())
