import pytest
from app.schemas import UserCreate, AccountCreate, UserUpdate, AccountUpdate
from app.service import UserService, AccountService
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from sqlmodel import Session, select, func
from app.models import User, Account
from app.exceptions import CannotDeleteUserWithAccounts
def test_can_not_change_user_email(session, default_user):    
    service = UserService(session)
    created_user = service.create(default_user)

    assert created_user.email == "test1@ejemplo.com"
    with pytest.raises(ValidationError):
        updated_user = UserUpdate(email = "test2@ejemplo.com")
        service.update(1, updated_user)

    assert created_user.email == "test1@ejemplo.com"