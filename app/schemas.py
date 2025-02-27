from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from fastapi import Form, File, UploadFile

class SummaryRequest(BaseModel):
    book_id: int

class SummaryResponse(BaseModel):
    summary: str

class ReviewBase(BaseModel):
    user_id: int
    review_text: str
    rating: float

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class BookBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    year_published: Optional[int] = None

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None
    text_content: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Sample Book",
                "author": "John Doe",
                "genre": "Fiction",
                "year_published": 2024,
                "summary": "Optional summary",
                "text_content": "Book content here..."
            }
        }
    )

class BookUpdate(BookBase):
    summary: Optional[str] = None
    text_content: Optional[str] = None

class Book(BaseModel):
    id: int
    title: str
    author: str
    genre: Optional[str] = None
    year_published: Optional[int] = None
    text_content: Optional[str] = None
    summary: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class BookSummary(BaseModel):
    summary: str
    average_rating: float
