import asyncio

from database import *
import model

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(model.Base.metadata.create_all) #dessa forma engloba todos os Base
        print("criou")


if __name__ == "__main__":
    asyncio.run(create_tables())
