
from sqlalchemy.future import select
from app.models import Book
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import logging

async def get_recommendations(db: AsyncSession, preferences: dict):
    logging.info("Fetching recommendations with preferences: %s", preferences)
    genre = preferences.get("genre")
    if genre:
         result = await db.execute(select(Book).where(Book.genre == genre))
         books = result.scalars().all()
         logging.info("Found %d books for genre: %s", len(books), genre)
         return books
    else:
         result = await db.execute(select(Book))
         books = result.scalars().all()
         logging.info("Found %d books with no genre filter", len(books))
         return books
