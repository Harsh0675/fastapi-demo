# FastAPI REST API

A production-oriented REST API built with **FastAPI**, **SQLite**, **JWT authentication**, and **Argon2 password hashing**.

## 🚀 Live Demo

- **Live API:** https://fastapi-demo-production.up.railway.app
- **Swagger UI:** https://fastapi-demo-production.up.railway.app/docs

## Features

- RESTful User CRUD
- JWT access-token authentication
- Secure password hashing with Argon2
- Request validation with Pydantic
- SQLite persistence
- Interactive Swagger/OpenAPI documentation
- Automated API tests with pytest
- Environment-based secrets via `.env`

## Project structure

```text
fastapi-demo/
├── app/
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── main.py
│   └── routes/
│       ├── auth.py
│       └── users.py
├── tests/
│   └── test_api.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000`

Swagger UI: `http://127.0.0.1:8000/docs`

## Test

```bash
pytest -q
```

## Authentication

Create a `.env` file containing a strong secret:

```env
SECRET_KEY=replace-with-a-strong-random-secret
```

Never commit `.env` or real secrets. The repository ignores `.env` by default.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API status |
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Login and receive JWT |
| GET | `/auth/me` | Get authenticated user |
| POST | `/users` | Create user |
| GET | `/users` | List users |
| GET | `/users/{user_id}` | Get user |
| PUT | `/users/{user_id}` | Update user |
| DELETE | `/users/{user_id}` | Delete user |

## Tech stack

Python 3 · FastAPI · Pydantic · SQLite · JWT · Argon2 · pytest · Uvicorn
