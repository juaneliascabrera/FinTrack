import pytest
from app.exceptions import (
    CannotDeleteAccountWithBalance,
    CannotDeleteUserWithAccounts,
    IncorrectPassword,
)
from app.models import Account, User
from app.schemas import UserUpdate
from app.security import verify_password
from app.service import AccountService, UserService
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, func, select


def users_amount(session: Session):
    # We use the SQL count function
    consulta = select(func.count()).select_from(User)
    cantidad = session.exec(consulta).one()
    return cantidad


def accounts_amount(session: Session):
    # We use the SQL count function
    consulta = select(func.count()).select_from(Account)
    cantidad = session.exec(consulta).one()
    return cantidad


def test_can_create_user(session, default_user):

    service = UserService(session)
    assert users_amount(session) == 0
    created_user = service.create(default_user)

    assert users_amount(session) == 1
    assert created_user.id is not None
    assert created_user.email == "test1@ejemplo.com"


def test_can_change_user_name(session, default_user):
    service = UserService(session)
    created_user = service.create(default_user)

    assert created_user.name == "Juan"
    updated_user = UserUpdate(name="Elias")
    service.update(1, updated_user)
    # Now assert name has changed
    assert created_user.name == "Elias"


def test_can_change_user_password(session, default_user):
    service = UserService(session)
    created_user = service.create(default_user)

    assert verify_password("123", created_user.password)
    updated_user = UserUpdate(password="321")
    service.update(1, updated_user)
    # Now assert password has changed
    assert verify_password("321", created_user.password)


def test_can_create_account(session, default_user, account_factory):
    account_service = AccountService(session)
    user_service = UserService(session)

    created_user = user_service.create(default_user)

    new_account = account_factory(user_id=created_user.id, balance=500)

    created_account = account_service.create(new_account)

    assert created_account.id is not None
    assert created_account.name == "MercadoPago"
    assert created_account.balance == 500


def test_list_all_works(session, default_user):
    user_service = UserService(session)
    assert len(user_service.list_all()) == 0
    user_service.create(default_user)

    assert len(user_service.list_all()) == 1


def test_an_user_can_add_an_account(session, default_user, account_factory):
    # Prepare
    user_service = UserService(session)
    account_service = AccountService(session)

    created_user = user_service.create(default_user)
    # Pre-asserts
    assert len(created_user.accounts) == 0

    new_account = account_factory(user_id=created_user.id, balance=1000)
    created_account = account_service.create(new_account)

    # Post-asserts
    assert len(created_user.accounts) == 1
    assert created_account.user_id == created_user.id
    assert created_account.name == "MercadoPago"
    assert created_account.balance == 1000


def test_creating_account_with_invalid_user_id_raises_integrity_error(
    session, default_user, account_factory
):
    account_service = AccountService(session)
    user_service = UserService(session)

    created_user = user_service.create(default_user)

    # Pre-asserts
    assert len(created_user.accounts) == 0
    new_account = account_factory(user_id=999, balance=1000)

    with pytest.raises(IntegrityError):
        account_service.create(new_account)
    session.rollback()
    # Post-asserts
    assert len(created_user.accounts) == 0


def test_can_delete_user_if_has_no_accounts(session, default_user):
    AccountService(session)
    user_service = UserService(session)

    created_user = user_service.create(default_user)

    # Assert user exists
    assert users_amount(session) == 1

    # Deleting
    user_service.delete_user_safe(created_user.id)

    # Assert user doesn't exists anymore.
    assert users_amount(session) == 0


def test_can_not_delete_user_if_has_accounts(session, default_user, account_factory):
    account_service = AccountService(session)
    user_service = UserService(session)

    created_user = user_service.create(default_user)

    new_account = account_factory(user_id=created_user.id, balance=1000)
    created_account = account_service.create(new_account)
    # Pre-assert
    assert created_account.balance == 1000
    # Try to delete
    with pytest.raises(CannotDeleteUserWithAccounts):
        user_service.delete_user_safe(created_user.id)
    # Post assert
    assert users_amount(session) == 1
    assert accounts_amount(session) == 1
    assert created_account.balance == 1000


def test_can_delete_account_if_it_has_no_balance(
    session, default_user, account_factory
):
    account_service = AccountService(session)
    user_service = UserService(session)

    created_user = user_service.create(default_user)
    new_account = account_factory(user_id=created_user.id, balance=0)
    created_account = account_service.create(new_account)
    # Assert
    assert created_account is not None
    assert created_account.balance == 0
    # Try
    account_service.delete_account_safe(created_account.id, created_user.id)
    # Assert
    assert accounts_amount(session) == 0


def test_can_not_delete_account_if_it_has_balance(
    session, default_user, account_factory
):
    account_service = AccountService(session)
    user_service = UserService(session)

    created_user = user_service.create(default_user)
    new_account = account_factory(user_id=created_user.id, balance=1000)
    created_account = account_service.create(new_account)
    # Assert
    assert created_account is not None
    assert created_account.balance == 1000
    # Try
    with pytest.raises(CannotDeleteAccountWithBalance):
        account_service.delete_account_safe(created_account.id, created_user.id)
    # Assert
    assert accounts_amount(session) == 1


def test_can_auth_correctly(session, default_user):
    user_service = UserService(session)
    created_user = user_service.create(default_user)
    # Password is 123

    authed_user = user_service.authenticate_user(
        created_user.email, default_user.password
    )

    assert authed_user is not None


def test_incorrect_password_raises_exception(session, default_user):
    user_service = UserService(session)
    created_user = user_service.create(default_user)
    # Password is 123

    with pytest.raises(IncorrectPassword):
        user_service.authenticate_user(created_user.email, "incorrect_pw")
