# ...existing code...
from sqlmodel import Session, SQLModel, create_engine

from .config import settings

# Engine configuration for PostgreSQL
# Force SSL for serverless environments
connect_args = {"sslmode": "require"}

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args=connect_args,
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# ...existing code...
