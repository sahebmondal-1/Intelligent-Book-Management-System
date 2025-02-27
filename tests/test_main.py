import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BASE_URL = os.getenv("BASE_URL", "http://test")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "secret")

pytest_plugins = "pytest_asyncio"

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        # Set basic authentication credentials for the test client
        client.auth = (ADMIN_USERNAME, ADMIN_PASSWORD)
        yield client

@pytest.mark.asyncio
async def test_read_books(test_client):
    response = test_client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_add_book(test_client):
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "genre": "Fiction",
        "year_published": 2024,
        "text_content": "Sample content"
    }
    response = test_client.post("/books", json=book_data)
    assert response.status_code == 200
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_get_book(test_client):
    book_id = 1  # Ensure this book exists in test DB
    response = test_client.get(f"/books/{book_id}")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert response.json()["id"] == book_id

@pytest.mark.asyncio
async def test_update_book(test_client):
    book_id = 4 
    update_data = {
  "author": "John Doe",
  "genre": "Fiction",
  "text_content": "Book content here...",
  "title": "Sample Book",
  "year_published": 2024
}
    response = test_client.put(f"/books/{book_id}", json=update_data)
    assert response.status_code == 200
    assert "id" in response.json()
    
@pytest.mark.asyncio
async def test_delete_book(test_client):
    book_id = 1  # Ensure this book exists in test DB
    response = test_client.delete(f"/books/{book_id}")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert response.json()["detail"] == "Book deleted"

@pytest.mark.asyncio
async def test_get_recommendations(test_client):
    response = test_client.get("/recommendations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_generate_summary(test_client):
    book_id = 1  # Ensure this book exists in test DB
    request_data = {"book_id": book_id}
    response = test_client.post("/generate-summary", json=request_data)
    assert response.status_code in [200, 404, 400]
    if response.status_code == 200:
        assert "summary" in response.json()

@pytest.mark.asyncio
async def test_get_reviews(test_client):
    book_id = 1  # Ensure this book exists in test DB
    response = test_client.get(f"/books/{book_id}/reviews")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_add_review(test_client):
    book_id = 1  # Ensure this book exists in test DB
    review_data = {
        "user_id": 1,
        "review_text": "Great book!",
        "rating": 4.5
    }
    response = test_client.post(f"/books/{book_id}/reviews", json=review_data)
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert "id" in response.json()
