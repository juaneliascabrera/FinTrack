import pytest
from app.schemas import UserCreate, AccountCreate
from app.service import UserService, AccountService
def test_can_create_user(session):

    service = UserService(session)
    new_user = UserCreate(name = "Juan", email = "test1@ejemplo.com", password = "123")
    
    created_user = service.create(new_user)

    assert created_user.id is not None
    assert created_user.email == "test1@ejemplo.com"

def test_can_create_account(session):
    service = AccountService(session)
    new_account = AccountCreate(name = "MercadoPago", balance = 1000)
    
    created_account = service.create(new_account)

    assert created_account.id is not None
    assert created_account.name == "MercadoPago"
    assert created_account.balance == 1000