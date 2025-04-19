from rich.console import Console
from tortoise import Tortoise
from contextlib import asynccontextmanager

console = Console()


@asynccontextmanager
async def db_context(db_url: str):
    try:
        await Tortoise.init(
            db_url=db_url, modules={"models": ["upwork_fetcher.models"]}
        )
        await Tortoise.generate_schemas(safe=True)
        # console.print("Tortoise-ORM started")
        yield
    finally:
        await Tortoise.close_connections()


# Usage example:
# async with db_context():
#     # your database operations here
