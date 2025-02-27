# Intelligent Book Management System

## Overview

The Intelligent Book Management System is a FastAPI-based application that enables users to manage a collection of books. It offers endpoints for:

- **Book CRUD Operations:** Create, read, update, and delete books.
- **Review Management:** Add and retrieve reviews for books.
- **Summary Generation:** Generate summaries from book content using an open-source language model (LLM).
- **Recommendations:** Retrieve book recommendations based on genre.
- **Authentication:** Secures endpoints using HTTP Basic authentication.
- **Logging:** Application logs are stored in `/mnt/logs/app.log`.
- **Configuration:** Sensitive credentials and other configuration variables are managed via a `.env` file.
- **Testing:** Automated tests are implemented using pytest and pytest-asyncio.

## Features

- **FastAPI & Uvicorn:** Robust, high-performance API server.
- **SQLAlchemy (Async):** Asynchronous interactions with your PostgreSQL database.
- **Pydantic (v2):** Data validation with updated configurations.
- **Swagger UI:** Interactive API documentation available at `/docs`.
- **Environment Configuration:** Managed via a `.env` file for secure, flexible deployments.
- **Open Source LLM for Summary Generation:** Book summaries are generated using an open-source language model (LLM) integrated via Ollama.
- **Automated Testing:** Comprehensive tests to ensure API functionality.

## Prerequisites

- Python 3.10+ (tested on Python 3.12)
- PostgreSQL (or another compatible database; update `DATABASE_URL` as needed)
- Virtual Environment (recommended)
- Ollama (for model-based processing)

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/sahebmondal-1/Intelligent-Book-Management-System.git
   cd AI-Book-Management-System
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the project root with the following content (modify values as needed):

   ```ini
   DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/bookdb
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=secret
   LOG_DIR=/mnt/logs
   BASE_URL=http://localhost:8000
   ```

5. **Set Up the Database**

   Ensure your database is running and accessible using the connection details provided in the `.env` file.

## Running the Application

Start the application using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be accessible at: [http://localhost:8000](http://localhost:8000)

## API Documentation

FastAPI automatically provides interactive API documentation with Swagger UI.  
Access it at: [http://localhost:8000/docs](http://localhost:8000/docs)

## Running Tests

Automated tests are implemented with pytest.

Run all tests with:

```bash
pytest -v tests/
```

## Project Structure

```
AI-Book-Management-System/
├── app/
│   ├── __init__.py             # Marks the app directory as a package
│   ├── main.py                 # Application entry point
│   ├── crud.py                 # CRUD operations for books and reviews
│   ├── models.py               # Database models (SQLAlchemy)
│   ├── database.py             # Database connection setup
│   ├── config.py               # Logging and environment configuration
│   ├── auth.py                 # Authentication
│   ├── schemas.py              # Pydantic models for requests/responses
│   └── recommendations.py      # Recommendation logic based on book genre
├── tests/
│   └── test_main.py            # Automated test cases
├── .env                        # Environment variables
├── pytest.ini                  # Pytest configuration (set asyncio loop scope)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```



## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.