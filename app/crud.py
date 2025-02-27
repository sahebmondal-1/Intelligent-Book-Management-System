from app.config import logging
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Book, Review

async def create_book(db: AsyncSession, book: Book) -> Book:
    logging.info("Creating book: %s", book.title)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    logging.info("Book created with id: %s", book.id)
    return book

async def get_books(db: AsyncSession):
    logging.info("Fetching all books")
    result = await db.execute(select(Book))
    books = result.scalars().all()
    logging.info("Fetched %d books", len(books))
    return books

async def get_book(db: AsyncSession, book_id: int):
    logging.info("Fetching book with id: %d", book_id)
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if book:
        logging.info("Book found with id: %d", book_id)
    else:
        logging.warning("No book found with id: %d", book_id)
    return book

async def update_book(db: AsyncSession, book: Book):
    logging.info("Updating book with id: %d", book.id)
    # No need to add or merge the book again—it's already attached.
    await db.commit()
    await db.refresh(book)
    logging.info("Book with id %d updated", book.id)
    return book

async def delete_book(db: AsyncSession, book: Book):
    logging.info("Deleting book with id: %d", book.id)
    await db.delete(book)
    await db.commit()
    logging.info("Book with id %d deleted", book.id)

async def create_review(db: AsyncSession, review: Review) -> Review:
    logging.info("Creating review for book id: %d", review.book_id)
    db.add(review)
    await db.commit()
    await db.refresh(review)
    logging.info("Review created with id: %d", review.id)
    return review

async def get_reviews(db: AsyncSession, book_id: int):
    logging.info("Fetching reviews for book id: %d", book_id)
    result = await db.execute(select(Review).where(Review.book_id == book_id))
    reviews = result.scalars().all()
    logging.info("Fetched %d reviews for book id: %d", len(reviews), book_id)
    return reviews
