#from .models import User
from .schemas import UserCreate, AccountCreate
from sqlmodel import Session, SQLModel, select
from .models import User, Account
from .exceptions import NotExistsError, CannotDeleteUserWithAccounts, CannotDeleteAccountWithBalance
from typing import Generic, TypeVar, Type
T = TypeVar("T", bound=SQLModel)

class Service(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model
    # Shared methods
    def list_all(self):
        instruction = select(self.model)
        return self.session.exec(instruction).all()

    def create(self, data):
        db_obj = self.model(**data.model_dump())
        self.session.add(db_obj)
        try:
            self.session.commit()
            self.session.refresh(db_obj)
        except Exception as exc:
            self.session.rollback()
            raise exc
        
        return db_obj
    
    def get_by_id(self, id: int):
        return self.session.get(self.model, id)

    def delete(self, obj_id):
        raise NotImplementedError("Subclass responsibility")

    def update(self, id, data):
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for llave, valor in update_data.items():
            setattr(db_obj, llave, valor)

        self.session.add(db_obj)
        try:
            self.session.commit()
            self.session.refresh(db_obj)
        except Exception as exc:
            self.session.rollback()
            raise exc
        return db_obj

class UserService(Service[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def delete(self, user_id):
        user_obj = self.session.get(self.model, user_id)
        if not user_obj:
            raise NotExistsError
        if user_obj.accounts:
            raise CannotDeleteUserWithAccounts
        self.session.delete(user_obj)
        try:
            self.session.commit()
        except Exception as exc:
            self.session.rollback()
            raise exc
        return True
        
class AccountService(Service[Account]):
    def __init__(self, session: Session):
        super().__init__(session, Account)

    def delete(self, account_id):
        account_obj = self.session.get(self.model, account_id)
        if not account_obj:
            raise NotExistsError
        if account_obj.balance != 0:
            raise CannotDeleteAccountWithBalance
        self.session.delete(account_obj)
        try:
            self.session.commit()
        except Exception as exc:
            self.session.rollback()
            raise exc
        return True