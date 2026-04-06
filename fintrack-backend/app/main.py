from fastapi import FastAPI, Depends, HTTPException, status, Response, Request 
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from .service import UserService, AccountService
from sqlmodel import Session
from .schemas import *
from .database import get_session, create_db_and_tables
from .exceptions import *
from .security import create_access_token, decode_access_token
from .models import User
from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
app = FastAPI(lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Exception handler
@app.exception_handler(NotExistsError)
async def not_exists_exception_handler(request: Request, exc: NotExistsError):
    return JSONResponse(
        status_code=404,
        content={"detail": "The solicited resource does not exists"}
    )
@app.exception_handler(CannotDeleteUserWithAccounts)
async def delete_conflict_exception_handler(request: Request, exc: CannotDeleteUserWithAccounts):
    return JSONResponse(
        status_code=409,
        content={"detail": "Can't delete user because it has active accounts."}
    )
@app.exception_handler(CannotDeleteAccountWithBalance)
async def delete_conflict_exception_handler(request: Request, exc: CannotDeleteAccountWithBalance):
    return JSONResponse(
        status_code=409,
        content={"detail": "Can't delete account because it has balance."}
    )

@app.exception_handler(IncorrectPassword)
async def incorrect_password_exception_handler(request: Request, exc: IncorrectPassword):
    return JSONResponse(
        status_code=401,
        content={"detail": "The password is incorrect."}
    )

# -- Services --

def get_user_service(session: Session = Depends(get_session)):
    return UserService(session)

def get_account_service(session: Session = Depends(get_session)):
    return AccountService(session)

def get_current_user(token: str = Depends(oauth2_scheme), service: UserService = Depends(get_user_service)):
    payload = decode_access_token(token)

    if not payload or not payload.get("sub"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid session", 
        headers={"WWW-Authenticate": "Bearer"},
        )
    user = service.get_by_email(payload.get("sub"))

    if not user:
        raise HTTPException(status_code=401, detail = "User not found")

    return user
    

# Login
@app.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service)):
    # Trying to authenticate
    user = service.authenticate_user(form_data.username, form_data.password)
    # If it was correct
    access_token = create_access_token(data={"sub": user.email})

    # Returning token
    return {"access_token": access_token, "token_type": "bearer"}

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

@app.delete("/users/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    service.delete(user_id)
    return Response(status_code = 204)
    
    
# Account endpoints
@app.post("/accounts", response_model=AccountPublic, status_code=201)
def create_account(data: AccountCreate, 
service: AccountService = Depends(get_account_service),
current_user = Depends(get_current_user)
):
    account_data = data.model_dump()
    account_data["user_id"] = current_user.id
    return service.create_with_owner(account_data)

@app.get("/accounts", response_model=list[AccountPublic])
def list_accounts(
    service: AccountService = Depends(get_account_service),
    current_user: User = Depends(get_current_user)
):
    return service.list_all()

@app.patch("/accounts/{account_id}", response_model=AccountPublic)
def update_account(account_id: int, data: AccountUpdate, 
service: AccountService = Depends(get_account_service),
current_user = Depends(get_current_user)):
    updated_account = service.update(account_id, data)
    if not updated_account:
        raise HTTPException(status_code=404, detail="Account Not Found")
    return updated_account

@app.delete("/accounts/{account_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, service: AccountService = Depends(get_account_service),
current_user = Depends(get_current_user)):
    service.delete(account_id)
    return Response(status_code = 204)

