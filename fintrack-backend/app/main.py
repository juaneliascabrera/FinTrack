from fastapi import FastAPI, Depends, HTTPException
from .service import UserService, AccountService
from sqlmodel import Session
from .schemas import UserCreate
from .database import get_session

app = FastAPI()

def get_user_service(session: Session = Depends(get_session)):
    return UserService(session)

def get_account_service(session: Session = Depends(get_session)):
    return AccountService(session)

@app.post("/users", response_model=UserPublic, status_code=201)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(data)


