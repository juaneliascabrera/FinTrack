# FinTrack API Backend

FinTrack is a robust and modern API designed for personal financial
tracking. It allows users to register, authenticate, create multiple
accounts, and record financial transactions (Income, Expenses, and
Transfers between accounts), all secured with JWT and built following
solid architectural practices.

## 🚀 Project Status

The project is in a **solid, development-ready state**. It correctly
implements:

-   **Layered Architecture:** Clear separation between controllers
    (FastAPI), services (business logic and database access), and
    models/schemas.\
-   **Strict Validation:** The combined use of Pydantic and SQLModel
    enforces strong typing at both the API and database levels.\
-   **Security & Integrity:** Password hashing with bcrypt, built-in SQL
    injection protection, and recursive ownership validation (a user
    cannot manipulate another user's resources, whether by mistake or
    intent).\
-   **Consistency:** Atomic database operations via *Dependency
    Injection* and request-scoped session instances.\
-   **Clean & Modern Environment:** Ultra-fast dependency management
    (via `uv`), containerized database, and comprehensive linting (via
    `ruff`).

------------------------------------------------------------------------

## 🛠️ Technologies Used

-   **Python 3.13**
-   **FastAPI**
-   **SQLModel / SQLAlchemy**
-   **PostgreSQL**
-   **Pytest**
-   **Ruff**
-   **Uv**
-   **Docker & Docker Compose**

------------------------------------------------------------------------

## 📂 Project Structure

    proyecto-fintrack/
    ├── fintrack-backend/
    │   ├── app/
    │   │   ├── main.py
    │   │   ├── models.py
    │   │   ├── schemas.py
    │   │   ├── service.py
    │   │   ├── security.py
    │   │   ├── database.py
    │   │   ├── config.py
    │   │   └── exceptions.py
    │   └── tests/
    ├── pyproject.toml
    ├── docker-compose.yml
    ├── uv.lock
    └── .env

------------------------------------------------------------------------

## ⚙️ Installation and Setup (Local)

### 1. Environment Variables

``` ini
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/fintrack
SECRET_KEY=your_very_secure_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. Dockerized Database

``` bash
docker compose up -d
```

### 3. Environment & Installation

``` bash
uv sync
```

### 4. Run the Server

``` bash
source .venv/bin/activate
uvicorn fintrack-backend.app.main:app --reload
```

------------------------------------------------------------------------

## 🧪 Testing and Linting

``` bash
pytest fintrack-backend/tests
ruff check .
ruff format .
```

------------------------------------------------------------------------

## 📑 Domain Model

-   **Users (`User`)**
-   **Accounts (`Account`)**
-   **Transactions (`Transaction`)**
