import pytest
from app.schemas import AccountCreate, UserCreate
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture(name="session")
def session_fixture():
    # 1. Creamos el motor en memoria
    # El StaticPool es el truco para que SQLite no se "olvide" de los datos
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )

    # 2. Creamos las tablas (User, Account, etc.)
    SQLModel.metadata.create_all(engine)

    # 3. Abrimos la sesión para el test
    with Session(engine) as session:
        yield session  # El test usa la sesión aquí

    # 4. Al terminar el test, las tablas desaparecen de la RAM


@pytest.fixture
def default_user():
    return UserCreate(name="Juan", email="test1@ejemplo.com", password="123")


@pytest.fixture
def account_factory():
    def _make_account(user_id: int, balance: int = 1000):
        return AccountCreate(name="MercadoPago", balance=balance, user_id=user_id)

    return _make_account
