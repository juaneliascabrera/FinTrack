from fastapi import FastAPI, Depends, HTTPException
from .service import UserService
from .schemas import UserCreate, UserPublic, UserUpdate

app = FastAPI()

def get_user_service():
    pass
@app.post("/users", response_model = UserPublic, status_code=201)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(data)
