Here’s your enhanced README with some cool icons!  

---

# 📚 Intelligent Book Management System  

## 🚀 Overview  

The **Intelligent Book Management System** is a **FastAPI-based** application that enables users to manage a collection of books. It offers endpoints for:  

✅ **Book CRUD Operations** – Create, Read, Update, and Delete books.  
✅ **📝 Review Management** – Add and retrieve reviews for books.  
✅ **📖 Summary Generation** – Generate summaries using an open-source **LLM (Ollama)**.  
✅ **📚 Recommendations** – Get book recommendations based on genre.  
✅ **🔒 Authentication** – Secure endpoints with **HTTP Basic authentication**.  
✅ **📝 Logging** – Logs stored at `/mnt/logs/app.log`.  
✅ **⚙️ Configuration** – `.env` file for secure credentials & config.  
✅ **✅ Testing** – Automated tests with **pytest & pytest-asyncio**.  

## 🌟 Features  

🔹 **⚡ FastAPI & Uvicorn** – High-performance API server.  
🔹 **📡 SQLAlchemy (Async)** – Asynchronous PostgreSQL interactions.  
🔹 **✅ Pydantic v2** – Modern data validation & serialization.  
🔹 **📄 Swagger UI** – Interactive API docs at `/docs`.  
🔹 **🔐 Environment Configuration** – `.env` for flexible deployments.  
🔹 **🤖 AI-Powered Summaries** – Uses **Ollama** for summarizing books.  
🔹 **🧪 Automated Testing** – Ensures API reliability.  

---

## 🔧 Prerequisites  

✔️ **Python 3.10+** (tested on **Python 3.12**)  
✔️ **PostgreSQL** (update `DATABASE_URL` as needed)  
✔️ **Virtual Environment** (recommended)  
✔️ **Ollama** (for AI-based processing)  

---

## 🛠️ Setup Instructions  

### 1️⃣ Clone the Repository  

```bash
git clone https://github.com/sahebmondal-1/Intelligent-Book-Management-System.git
cd Intelligent-Book-Management-System
```

### 2️⃣ Create a Virtual Environment  

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies  

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables  

Create a **`.env`** file in the project root:  

```ini
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/bookdb
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secret
LOG_DIR=/mnt/logs
BASE_URL=http://localhost:8000
```

---

## ▶️ Running the Application  

Start the app using **Uvicorn**:  

```bash
nohup uvicorn app.main:app --host 0.0.0.0 --port 80 > /mnt/logs/server.log 2>&1 &
```

**🌍 API Access:** [http://localhost:8000](http://localhost:8000)  

### 📜 API Documentation  

FastAPI automatically generates Swagger UI at:  
📌 [http://localhost:8000/docs](http://localhost:8000/docs)  

---

## 🧪 Running Tests  

Run all tests using **pytest**:  

```bash
pytest -v tests/
```

---

## 📂 Project Structure  

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
│   ├── recommendations.py      # Recommendation logic based on book genre
├── tests/
│   └── test_main.py            # Automated test cases
├── .env                        # Environment variables
├── pytest.ini                  # Pytest configuration (set asyncio loop scope)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 📜 License  

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.  
