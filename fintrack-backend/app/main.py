from fastapi import FastAPI, Depends, HTTPException
from .service import UserService, AccountService
from sqlmodel import Session
from .schemas import UserCreate

app = FastAPI()

def get_user_service(session: Session = Depends(get_session)):
    return UserService(session)

def get_account_service(session: Session = Depends(get_session)):
    return AccountService(session)

