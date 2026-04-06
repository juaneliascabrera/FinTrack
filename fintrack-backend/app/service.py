#from .models import User
from .schemas import UserCreate, UserUpdate
from sqlmodel import Session, SQLModel, select
from .models import User, Account
from .exceptions import NotExistsError, CannotDeleteUserWithAccounts, CannotDeleteAccountWithBalance, IncorrectPassword
from typing import Generic, TypeVar, Type
from .security import *
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

    def create(self, data):
        db_obj = self.model(**data.model_dump())
        return self._save(db_obj)
    
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

        return self._save(db_obj)

class UserService(Service[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def get_by_email(self, email: str):
        statement = select(self.model).where(self.model.email == email)
        return self.session.exec(statement).first()

    def authenticate_user(self, email: str, plain_password: str):
        #We need to search the user by email
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
        
    def update(self, user_id: int, data: UserUpdate):
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        
        # If we have password
        if "password" in update_data and update_data["password"]:
            update_data["password"] = get_password_hash(update_data["password"])
            
        for llave, valor in update_data.items():
            setattr(db_user, llave, valor)

        return self._save(db_user)

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
    
