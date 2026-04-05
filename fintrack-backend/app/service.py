#from .models import User
from .schemas import UserCreate, AccountCreate
from sqlmodel import Session, SQLModel
from .models import User, Account
from .exceptions import NotExistsError, CannotDeleteUserWithAccounts
from typing import Generic, TypeVar, Type
T = TypeVar("T", bound=SQLModel)

class Service(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def create(self, data):
        db_obj = self.model(**data.model_dump())
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj
    
    def delete(self, obj_id):
        raise NotImplementedError("Subclass responsibility")

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
        self.session.commit()
        return True

class AccountService(Service[Account]):
    def __init__(self, session: Session):
        super().__init__(session, Account)

    