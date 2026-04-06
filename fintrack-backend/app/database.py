# ...existing code...
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from .config import settings

# Uso temporal: SQLite en memoria (RAM) para pruebas


engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# ...existing code...
