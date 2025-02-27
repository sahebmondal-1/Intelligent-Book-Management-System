from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn
from app.database import async_session, engine
from app.models import Base, Book, Review
from app.schemas import (
    BookCreate, 
    BookUpdate, 
    Book as BookSchema, 
    ReviewCreate, 
    Review as ReviewSchema, 
    BookSummary, 
    SummaryResponse, 
    SummaryRequest
)
from app.crud import (
    create_book, 
    get_books, 
    get_book, 
    update_book, 
    delete_book, 
    create_review, 
    get_reviews
)
from app.auth import get_current_user
from app.llama_integration import generate_summary
from app.recommendations import get_recommendations as fetch_recommendations
from app.config import logging
from contextlib import asynccontextmanager

# Lifespan event handler using the new pattern
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting application and creating database tables")
    async with engine.begin() as conn:
         await conn.run_sync(Base.metadata.create_all)
    yield
    # Add shutdown code here if needed

app = FastAPI(title="Intelligent Book Management System", lifespan=lifespan)

async def get_db():
    async with async_session() as session:
         yield session

@app.post("/books")
async def add_book(book: BookCreate, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_user)):
    logging.info("User %s is adding a new book: %s", username, book.title)
    book_data = {
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "year_published": book.year_published,
        "text_content": book.text_content
    }
    db_book = Book(**book_data)
    db_book = await create_book(db, db_book)
    logging.info("Book added successfully: %s", book.title)
    return db_book

@app.get("/books")
async def read_books(db: AsyncSession = Depends(get_db), username: str = Depends(get_current_user)):
    logging.info("User %s is fetching all books", username)
    books = await get_books(db)
    return books

@app.get("/books/{book_id}", response_model=BookSchema)
async def read_book(book_id: int, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_user)):
    logging.info("User %s is fetching book with id: %d", username, book_id)
    book = await get_book(db, book_id)
    if not book:
         logging.error("Book with id %d not found", book_id)
         raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=BookSchema)
async def update_book_endpoint(book_id: int, book_update: BookUpdate, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_user)):
    logging.info("User %s is updating book with id: %d", username, book_id)
    book = await get_book(db, book_id)
    if not book:
         logging.error("Book with id %d not found for update", book_id)
         raise HTTPException(status_code=404, detail="Book not found")
    # Use model_dump instead of dict to avoid Pydantic deprecation warnings
    for key, value in book_update.model_dump(exclude_unset=True).items():
         setattr(book, key, value)
    book = await update_book(db, book)
    logging.info("Book with id %d updated successfully", book_id)
    return book

@app.delete("/books/{book_id}")
async def delete_book_endpoint(book_id: int, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_user)):
    logging.info("User %s is deleting book with id: %d", username, book_id)
    book = await get_book(db, book_id)
    if not book:
         logging.error("Book with id %d not found for deletion", book_id)
         raise HTTPException(status_code=404, detail="Book not found")
    await delete_book(db, book)
    logging.info("Book with id %d deleted successfully", book_id)
    return {"detail": "Book deleted"}

@app.post("/books/{book_id}/reviews", response_model=ReviewSchema)
async def add_review(book_id: int, review: ReviewCreate, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_user)):
    logging.info("User %s is adding a review for book id: %d", username, book_id)
    book = await get_book(db, book_id)
    if not book:
         logging.error("Book with id %d not found for review", book_id)
         raise HTTPException(status_code=404, detail="Book not found")
    db_review = Review(book_id=book_id, **review.dict())
    db_review = await create_review(db, db_review)
    logging.info("Review added for book id: %d", book_id)
    return db_review

@app.get("/books/{book_id}/reviews", response_model=list[ReviewSchema])
async def read_reviews(book_id: int, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_user)):
    logging.info("User %s is fetching reviews for book id: %d", username, book_id)
    reviews = await get_reviews(db, book_id)
    return reviews

@app.get("/books/{book_id}/summary", response_model=BookSummary)
async def get_book_summary(book_id: int, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_user)):
    logging.info("User %s is fetching summary for book id: %d", username, book_id)
    book = await get_book(db, book_id)
    if not book:
         logging.error("Book with id %d not found for summary", book_id)
         raise HTTPException(status_code=404, detail="Book not found")
    reviews = await get_reviews(db, book_id)
    avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0.0
    return BookSummary(summary=book.summary, average_rating=avg_rating)

@app.get("/recommendations", response_model=list[BookSchema])
async def recommendations(genre: str = None, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_user)):
    logging.info("User %s is fetching recommendations with genre: %s", username, genre)
    prefs = {"genre": genre} if genre else {}
    books = await fetch_recommendations(db, prefs)
    return books

@app.post("/generate-summary", response_model=SummaryResponse)
async def generate_summary_endpoint(request: SummaryRequest, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_user)):
    logging.info("User %s is generating summary for book id: %d", username, request.book_id)
    book = await get_book(db, request.book_id)
    if not book:
        logging.error("Book with id %d not found for summary generation", request.book_id)
        raise HTTPException(status_code=404, detail="Book not found")
    if not getattr(book, "text_content", None):
        logging.error("No text content available for book id: %d", request.book_id)
        raise HTTPException(status_code=400, detail="No text content available for this book")
    
    summary = await generate_summary(book.text_content)
    book.summary = summary
    book = await update_book(db, book)
    logging.info("Summary generated and updated for book id: %d", request.book_id)
    return SummaryResponse(summary=summary)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
