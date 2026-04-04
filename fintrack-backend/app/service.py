#from .models import User
from .schemas import UserCreate

class UserService:
    def __init__(self, db):
        self.db = db

    def create_user(self, user_data = UserCreate):
        id = max(self.db.keys() or [0]) + 1
        new_user = user_data.model_dump(exclude_unset=True)
        new_user["id"] = id
        new_user["accounts"] = []
        self.db[id] = new_user
        return new_user