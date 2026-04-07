# from .models import User
from typing import Generic, Type, TypeVar

from sqlmodel import Session, SQLModel, select

from .exceptions import (
    CannotDeleteAccountWithBalance,
    CannotDeleteUserWithAccounts,
    ForbiddenError,
    IncorrectPassword,
    InsufficientFunds,
    NotExistsError,
)
from .models import Account, Transaction, TransactionType, User
from .schemas import (
    AccountCreate,
    AccountUpdate,
    TransactionCreate,
    UserCreate,
    UserUpdate,
)
from .security import get_password_hash, verify_password

T = TypeVar("T", bound=SQLModel)


class Service(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    # Shared methods
    def _save(self, db_obj: T):
        self.session.add(db_obj)
        try:
            self.session.commit()
            self.session.refresh(db_obj)
        except Exception as exc:
            self.session.rollback()
            raise exc
        return db_obj

    def list_all(self):
        instruction = select(self.model)
        return self.session.exec(instruction).all()

    def list_accounts_of(self, user_id: int):
        instruction = select(Account).where(Account.user_id == user_id)
        results = self.session.exec(instruction)
        return results.all()

    def create(self, data):
        db_obj = self.model(**data.model_dump())
        return self._save(db_obj)

    def get_by_id(self, id: int):
        return self.session.get(self.model, id)

    def delete(self, db_obj: T):
        self.session.delete(db_obj)
        try:
            self.session.commit()
        except Exception as exc:
            self.session.rollback()
            raise exc
        return True

    def update(self, db_obj: T, data):
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)

        return self._save(db_obj)


class UserService(Service[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def get_by_email(self, email: str):
        statement = select(self.model).where(self.model.email == email)
        return self.session.exec(statement).first()

    def authenticate_user(self, email: str, plain_password: str):
        # We need to search the user by email
        user = self.get_by_email(email)
        if not user:
            raise NotExistsError
        if not verify_password(plain_password, user.password):
            raise IncorrectPassword

        return user

    def create(self, data: UserCreate):
        user_data = data.model_dump()
        user_data["password"] = get_password_hash(user_data["password"])
        db_user = self.model(**user_data)
        return self._save(db_user)

    def delete_user_safe(self, user_id):
        user_obj = self.session.get(self.model, user_id)
        if not user_obj:
            raise NotExistsError
        if user_obj.accounts:
            raise CannotDeleteUserWithAccounts
        return self.delete(user_obj)

    def update(self, user_id: int, data: UserUpdate):
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None

        update_data = data.model_dump(exclude_unset=True)

        # If we have password
        if "password" in update_data and update_data["password"]:
            update_data["password"] = get_password_hash(update_data["password"])

        for key, value in update_data.items():
            setattr(db_user, key, value)

        return self._save(db_user)


class AccountService(Service[Account]):
    def __init__(self, session: Session):
        super().__init__(session, Account)

    def _get_owned_account(self, account_id: int, user_id: int):
        account = self.get_by_id(account_id)
        if not account:
            raise NotExistsError
        if account.user_id != user_id:
            raise ForbiddenError
        return account

    def update_balance(self, account_id: int, amount: float):
        account = self.get_by_id(account_id)
        if not account:
            raise NotExistsError
        account.balance += amount
        self.session.add(account)
        # The TransactionService should make the commit.

    def delete_account_safe(self, account_id, user_id):
        account_obj = self._get_owned_account(account_id, user_id)
        if account_obj.balance != 0:
            raise CannotDeleteAccountWithBalance
        return self.delete(account_obj)

    def update_account_safe(self, account_id: int, data: AccountUpdate, user_id: int):
        account_obj = self._get_owned_account(account_id, user_id)
        return self.update(account_obj, data)

    def create_with_owner(self, account_data: AccountCreate):
        db_account = self.model(**account_data)
        return self._save(db_account)


class TransactionService(Service[Transaction]):
    def __init__(self, session: Session, account_service: AccountService):
        super().__init__(session, Transaction)
        self.account_service = account_service

    def _get_owned_transaction(self, account_id: int, user_id: int):
        transaction = self.get_by_id(account_id)
        if not transaction:
            raise NotExistsError
        if transaction.source_account != user_id:
            raise ForbiddenError
        return transaction

    def create_transaction(self, data: TransactionCreate, user_id: int):
        source_account = self.account_service.get_by_id(data.source_account)
        if not source_account or source_account.user_id != user_id:
            raise ForbiddenError()

        if data.type == TransactionType.TRANSFER:
            destination_account = self.account_service.get_by_id(
                data.destination_account
            )
            if not destination_account:
                raise NotExistsError()

        if data.type == TransactionType.INCOME:
            # We update our balance
            self.account_service.update_balance(data.source_account, data.amount)
        elif data.type == TransactionType.EXPENSE:
            # First we must check if we have enough balance
            if source_account.balance < data.amount:
                raise InsufficientFunds()
            # We update our balance
            self.account_service.update_balance(data.source_account, -data.amount)

        elif data.type == TransactionType.TRANSFER:
            if source_account.balance < data.amount:
                raise InsufficientFunds()
            self.account_service.update_balance(data.source_account, -data.amount)
            self.account_service.update_balance(data.destination_account, data.amount)
        db_transaction = Transaction(**data.model_dump())
        return self._save(db_transaction)

    def delete_transaction_safe(self, transaction_id: int, user_id: int):
        transaction_obj = self._get_owned_transaction(transaction_id, user_id)
        if transaction_obj is None:
            raise NotExistsError()
        return self.delete(transaction_obj)
