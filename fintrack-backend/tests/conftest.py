import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool
from app.main import app


@pytest.fixture(name="session")
def session_fixture():
    # 1. Creamos el motor en memoria
    # El StaticPool es el truco para que SQLite no se "olvide" de los datos
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    
    # 2. Creamos las tablas (User, Account, etc.)
    SQLModel.metadata.create_all(engine)
    
    # 3. Abrimos la sesión para el test
    with Session(engine) as session:
        yield session # El test usa la sesión aquí
        
    # 4. Al terminar el test, las tablas desaparecen de la RAM