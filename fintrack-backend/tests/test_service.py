import pytest
from app.schemas import UserCreate, AccountCreate
from app.service import UserService, AccountService
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select, func
from app.models import User, Account
from app.exceptions import CannotDeleteUserWithAccounts
def users_amount(session: Session):
    #Usamos la función count de SQL
    consulta = select(func.count()).select_from(User)
    cantidad = session.exec(consulta).one()
    return cantidad

def accounts_amount(session: Session):
    #Usamos la función count de SQL
    consulta = select(func.count()).select_from(Account)
    cantidad = session.exec(consulta).one()
    return cantidad

def get_new_user():
    return UserCreate(name = "Juan", email = "test1@ejemplo.com", password = "123")

def get_new_account_with_1000_balance(user_id: int):
    return AccountCreate(name = "MercadoPago", balance = 1000, user_id = user_id)

def get_new_account_with_0_balance(user_id: int):
    return AccountCreate(name = "MercadoPago", balance = 0, user_id = user_id)

def test_can_create_user(session):

    service = UserService(session)
    new_user = get_new_user()
    assert users_amount(session) == 0
    created_user = service.create(new_user)

    assert users_amount(session) == 1
    assert created_user.id is not None
    assert created_user.email == "test1@ejemplo.com"

def test_can_create_account(session):
    account_service = AccountService(session)
    user_service = UserService(session)    

    new_user = get_new_user()
    created_user = user_service.create(new_user)
    
    new_account = get_new_account_with_1000_balance(user_id = created_user.id)

    created_account = account_service.create(new_account)

    assert created_account.id is not None
    assert created_account.name == "MercadoPago"
    assert created_account.balance == 1000

def test_list_all_works(session):
    user_service = UserService(session)    
    assert len(user_service.list_all()) == 0
    new_user = get_new_user()
    created_user = user_service.create(new_user)

    assert len(user_service.list_all()) == 1
def test_an_user_can_add_an_account(session):
    #Prepare
    user_service = UserService(session)
    account_service = AccountService(session)

    new_user = get_new_user()
    created_user = user_service.create(new_user)
    #Pre-asserts
    assert len(created_user.accounts) == 0

    new_account = get_new_account_with_1000_balance(user_id = created_user.id)
    created_account = account_service.create(new_account)

    #Post-asserts
    assert len(created_user.accounts) == 1
    assert created_account.user_id == created_user.id
    assert created_account.name == "MercadoPago"
    assert created_account.balance == 1000

def test_creating_account_with_invalid_user_id_raises_integrity_error(session):
    account_service = AccountService(session)
    user_service = UserService(session)    

    new_user = get_new_user()
    created_user = user_service.create(new_user)

    #Pre-asserts
    assert len(created_user.accounts) == 0
    new_account = get_new_account_with_1000_balance(user_id = 999)

    with pytest.raises(IntegrityError):
        created_account = account_service.create(new_account)
    session.rollback()
    #Post-asserts
    assert len(created_user.accounts) == 0
    
#Testing cascade/restrict. 
#I will allow user deleting if and only if all his accounts have no balance.

def test_can_delete_user_if_has_no_accounts(session):
    account_service = AccountService(session)
    user_service = UserService(session)    

    new_user = get_new_user()
    created_user = user_service.create(new_user)

    #Assert user exists
    assert users_amount(session) == 1

    #Deleting
    user_service.delete(created_user.id)

    #Assert user doesn't exists anymore.
    assert users_amount(session) == 0

def test_can_not_delete_user_if_has_accounts(session):
    account_service = AccountService(session)
    user_service = UserService(session)    

    new_user = get_new_user()
    created_user = user_service.create(new_user)
    
    new_account = get_new_account_with_1000_balance(user_id = created_user.id)
    created_account = account_service.create(new_account)
    #Pre-assert
    assert created_account.balance == 1000
    #Try to delete
    with pytest.raises(CannotDeleteUserWithAccounts):
        user_service.delete(created_user.id)
    #Post assert
    assert users_amount(session) == 1
    assert accounts_amount(session) == 1
    assert created_account.balance == 1000