import pytest
from app.service import UserService
@pytest.fixture
def db_fake():
    # Una base de datos controlada para los tests
    return {
    1: {"name": "Elias", "id": 1, "accounts": ["fake_account_1"]},
    2: {"name": "Nat", "id": 2, "accounts": ["fake_account_2"]},
    }

@pytest.fixture
def service(db_fake):
    # Inyectamos la db_fake en el servicio
    return UserService(db_fake)