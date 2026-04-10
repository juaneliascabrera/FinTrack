import pytest
from app.schemas import AccountCreateTest, UserCreate
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
    # 1. Create the in-memory engine
    # StaticPool is the trick so SQLite doesn't "forget" the data
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )

    # 2. Create the tables (User, Account, etc.)
    SQLModel.metadata.create_all(engine)

    # 3. Open the session for the test
    with Session(engine) as session:
        yield session  # The test uses the session here

    # 4. When the test finishes, tables disappear from RAM


@pytest.fixture
def default_user():
    return UserCreate(name="Juan", email="test1@ejemplo.com", password="123")


@pytest.fixture
def account_factory():
    def _make_account(user_id: int, balance: int = 1000):
        temp_account = AccountCreateTest(
            name="MercadoPago", balance=balance, user_id=user_id
        )
        return temp_account

    return _make_account
