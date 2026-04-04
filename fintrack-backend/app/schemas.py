from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
class UserCreate(UserBase):
    name: str
    email: str
    password: str

class AccountBase(BaseModel):
    name: str | None = None
    balance: int | None = None
class AccountCreate(AccountBase):
    name: str
    balance: int