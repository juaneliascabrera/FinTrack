from fastapi import FastAPI, Depends, HTTPException
from .service import UserService, AccountService
from sqlmodel import Session
from .schemas import UserCreate, UserPublic, UserUpdate
from .database import get_session, create_db_and_tables
from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
app = FastAPI(lifespan=lifespan)


# -- Services --

def get_user_service(session: Session = Depends(get_session)):
    return UserService(session)

def get_account_service(session: Session = Depends(get_session)):
    return AccountService(session)

# User endpoints

@app.post("/users", response_model=UserPublic, status_code=201)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create(data)

@app.get("/users", response_model=list[UserPublic])
def list_users(
    service: UserService = Depends(get_user_service)
):
    return service.list_all()

@app.patch("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, data: UserUpdate, service: UserService = Depends(get_user_service)):
    updated_user = service.update(user_id, data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return updated_user