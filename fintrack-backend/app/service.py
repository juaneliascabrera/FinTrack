#from .models import User
from .schemas import UserCreate, AccountCreate
from sqlmodel import Session, SQLModel, select
from .models import User, Account
from .exceptions import NotExistsError, CannotDeleteUserWithAccounts
from typing import Generic, TypeVar, Type
T = TypeVar("T", bound=SQLModel)

class Service(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

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
        except Exception:
            self.session.rollback()
        return True
    
    def update(self, user_id, data):
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for llave, valor in update_data.items():
            setattr(db_user, llave, valor)

        self.session.add(db_user)
        try:
            self.session.commit()
            self.session.refresh(db_user)
        except Exception as exc:
            self.rollback()
            raise exc
        return db_user

class AccountService(Service[Account]):
    def __init__(self, session: Session):
        super().__init__(session, Account)

    