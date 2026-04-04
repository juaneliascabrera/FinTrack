#from .models import User
from .schemas import UserCreate
from sqlmodel import Session
from .models import User
class UserService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_data = UserCreate):
        new_user = User(**user_data.model_dump())
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
    
