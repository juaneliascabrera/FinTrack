import pytest
from app.schemas import AccountUpdate, UserUpdate
from app.service import AccountService, UserService
from pydantic import ValidationError


def test_can_not_change_user_email(session, default_user):
    service = UserService(session)
    created_user = service.create(default_user)

    assert created_user.email == "test1@ejemplo.com"
    with pytest.raises(ValidationError):
        updated_user = UserUpdate(email="test2@ejemplo.com")
        service.update(1, updated_user)

    assert created_user.email == "test1@ejemplo.com"


def test_can_not_change_account_balance(session, default_user, account_factory):
    user_service = UserService(session)
    account_service = AccountService(session)
    created_user = user_service.create(default_user)
    new_account = account_factory(user_id=created_user.id, balance=500)

    created_account = account_service.create(new_account)
    assert created_account.balance == 500
    with pytest.raises(ValidationError):
        updated_account = AccountUpdate(balance=10000)
        account_service.update(1, updated_account)

    assert created_account.balance == 500


def test_transaction_create_transfer_requires_destination():
    from app.schemas import TransactionCreate
    from app.models import TransactionType
    
    with pytest.raises(ValidationError):
        TransactionCreate(
            source_account=1,
            amount=500,
            type=TransactionType.TRANSFER,
            description="Transfer",
            # Missing destination_account
        )


def test_transaction_create_other_types_forbid_destination():
    from app.schemas import TransactionCreate
    from app.models import TransactionType
    
    with pytest.raises(ValidationError):
        TransactionCreate(
            source_account=1,
            destination_account=2,
            amount=500,
            type=TransactionType.INCOME,
            description="Salary"
        )


def test_transaction_amount_must_be_positive():
    from app.schemas import TransactionCreate
    from app.models import TransactionType
    
    with pytest.raises(ValidationError):
        TransactionCreate(
            source_account=1,
            amount=0,
            type=TransactionType.EXPENSE,
            description="Food"
        )
