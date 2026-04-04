import pytest
from app.schemas import UserCreate
from app.service import UserService
def test_can_create_user(session):

    service = UserService(session)
    new_user = UserCreate(name = "Juan", email = "test1@ejemplo.com", password = "123")
    
    created_user = service.create_user(new_user)

    assert created_user.id is not None
    assert created_user.email == "test1@ejemplo.com"

#def test_can_create_account(service, db_users_fake):