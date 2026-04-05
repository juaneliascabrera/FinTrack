# ...existing code...
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.pool import StaticPool

# Uso temporal: SQLite en memoria (RAM) para pruebas
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
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