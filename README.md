# 📝 Todolist App

A full-featured task management system built with **FastAPI** and **Streamlit**, backed by SQLite.  
Supports creating, editing, completing, and deleting tasks with optional deadlines and priority levels.

---

## 🚀 Features

### ✅ Backend (FastAPI)
- Add, update, delete tasks
- Mark tasks as completed or revert them
- SQLite database via SQLAlchemy
- Pydantic-based schema validation

### 💥 Frontend (Streamlit)
- Stylish to-do dashboard UI
- Task filtering and sorting
- Edit/delete/mark-complete buttons
- Optional deadlines and priority indicators

---

## 📁 Project Structure

```
Todolist/
├── UI.py                  # Streamlit frontend
├── main.py                # FastAPI app entrypoint
├── data.py                # Database connection logic
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── tasks.db               # SQLite database
└── .streamlit/config.toml # Streamlit config
```

---

## 💾 Setup Instructions

### 1. Clone the repository and install requirements

```bash
pip install -r requirements.txt
```

**Sample `requirements.txt`**

```
streamlit
fastapi
uvicorn
sqlalchemy
requests
```

---

### 2. Start the FastAPI backend

```bash
uvicorn main:app --reload
```

Server will be available at: `http://localhost:8000`

---

### 3. Run the Streamlit frontend

```bash
streamlit run UI.py
```

App will launch at: `http://localhost:8501`

---

## 🚰 Tech Stack

- Python 3.10+
- FastAPI for backend API
- Streamlit for UI
- SQLite (via SQLAlchemy) as database
- Pydantic for data validation

---

## 📌 Notes

- Tasks are stored in `tasks.db` SQLite file.
- You can tweak default settings in `.streamlit/config.toml`.

---

## 👨‍💻 Author

Built from scratch by me.  
Feel free to fork, explore, and enhance.
