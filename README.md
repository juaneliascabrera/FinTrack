# 💰 FinTrack

**FinTrack** is a full-stack personal finance tracker built with **FastAPI** and **React**. It allows users to register, authenticate, manage multiple accounts, and record financial transactions (income, expenses, and transfers) — all through a modern dark-themed dashboard.

![Dashboard Screenshot](fintrack-frontend/src/assets/hero.png)

---

## ✨ Features

- **JWT Authentication** — Secure login with token-based sessions and automatic expiration handling.
- **Multi-Account Management** — Create, list, and soft-delete financial accounts.
- **Transactions** — Record income, expenses, and transfers between accounts with automatic balance updates.
- **Dashboard** — Summary cards (total balance, income, expenses) and a recent transactions feed.
- **Responsive UI** — Dark premium design with glassmorphism, sidebar navigation, and mobile support.
- **Data Integrity** — Soft-delete accounts to preserve transaction history. Ownership validation on every operation.

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| **Python 3.13** | Runtime |
| **FastAPI** | REST API framework |
| **SQLModel / SQLAlchemy** | ORM and database models |
| **PostgreSQL** | Relational database |
| **Pydantic** | Request/response validation |
| **bcrypt + python-jose** | Password hashing and JWT |
| **uv** | Dependency management |
| **Ruff** | Linting and formatting |
| **Pytest** | Testing |
| **Docker Compose** | Containerized database |

### Frontend
| Technology | Purpose |
|---|---|
| **React 19** | UI library |
| **TypeScript** | Type safety |
| **Vite** | Build tool and dev server |
| **React Router v7** | Client-side routing |
| **Axios** | HTTP client with interceptors |
| **Vanilla CSS** | Custom design system with variables |

---

## 📂 Project Structure

```
proyecto-fintrack/
├── fintrack-backend/
│   ├── app/
│   │   ├── main.py          # Routes and exception handlers
│   │   ├── models.py         # SQLModel database models
│   │   ├── schemas.py        # Pydantic request/response schemas
│   │   ├── service.py        # Business logic layer
│   │   ├── security.py       # JWT and password hashing
│   │   ├── database.py       # Engine and session management
│   │   ├── config.py         # Environment settings
│   │   └── exceptions.py     # Custom domain exceptions
│   └── tests/
├── fintrack-frontend/
│   ├── src/
│   │   ├── components/       # DashboardLayout, Modals, Route guards
│   │   ├── context/          # AuthContext (global auth state)
│   │   ├── pages/            # Login, Home (Dashboard), Accounts
│   │   └── services/         # API client, auth, accounts, transactions
│   └── index.html
├── docker-compose.yml
├── pyproject.toml
└── .env
```

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.13+
- Node.js 18+
- Docker & Docker Compose
- [uv](https://docs.astral.sh/uv/) (Python package manager)

### 1. Clone and configure

```bash
git clone <repo-url>
cd proyecto-fintrack
```

Create a `.env` file in the project root:

```ini
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/fintrack
SECRET_KEY=your_very_secure_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. Start the database

```bash
docker compose up -d
```

### 3. Install and run the backend

```bash
uv sync
uv run uvicorn app.main:app --reload --app-dir fintrack-backend
```

The API will be available at `http://localhost:8000`. Interactive docs at `/docs`.

### 4. Install and run the frontend

```bash
cd fintrack-frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

---

## 🧪 Testing & Linting

```bash
# Run tests
uv run pytest fintrack-backend/tests

# Lint & format
uv run ruff check .
uv run ruff format .

# TypeScript check
cd fintrack-frontend && npx tsc --noEmit
```

---

## 📡 API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/login` | Authenticate and receive JWT |

### Users
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/users` | Register a new user |
| `GET` | `/users/me` | Get current user info |
| `PATCH` | `/users` | Update current user |
| `DELETE` | `/users` | Delete current user |

### Accounts
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/accounts` | Create a new account |
| `GET` | `/accounts` | List user's active accounts |
| `PATCH` | `/accounts/{id}` | Update account name |
| `DELETE` | `/accounts/{id}` | Soft-delete an account |
| `GET` | `/accounts/{id}/transactions` | List transactions for an account |

### Transactions
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/transactions` | List all user transactions (paginated) |
| `POST` | `/transactions` | Create a transaction |
| `DELETE` | `/transactions/{id}` | Delete and reverse a transaction |

---

## 📐 Architecture

```
Client (React) → Axios Interceptors → FastAPI Routes → Service Layer → SQLModel → PostgreSQL
```

- **Routes** (`main.py`): Handle HTTP, authentication, and response serialization.
- **Services** (`service.py`): Enforce business rules (ownership, balance checks, soft-delete).
- **Models** (`models.py`): Define database schema with relationships and validators.
- **Schemas** (`schemas.py`): Control what data enters and leaves the API.

---

## 📝 License

This project is for educational and personal use.
