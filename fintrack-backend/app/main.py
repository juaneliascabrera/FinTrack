from fastapi import FastAPI, Depends, HTTPException
from .service import UserService
from .schemas import UserCreate, UserPublic, UserUpdate

app = FastAPI()

db_temp = {
    1: {"name": "Elias", "id": 1, "accounts": ["fake_account_1"]},
    2: {"name": "Nat", "id": 2, "accounts": ["fake_account_2"]},
}

def get_user_service():
    pass
@app.post("/users", response_model = UserPublic, status_code=201)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(data)
