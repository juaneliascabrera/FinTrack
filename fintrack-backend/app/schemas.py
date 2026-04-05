from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
class UserCreate(UserBase):
    name: str
    email: EmailStr
    password: str

class UserPublic(UserBase):
    name: str
    email: EmailStr

class UserUpdate(UserBase):
    name: str | None = None
    password: str | None = None

class AccountBase(BaseModel):
    name: str | None = None
    balance: int | None = None

class AccountPublic(AccountBase):
    name: str
    balance: int

class AccountCreate(AccountBase):
    name: str
    balance: int
    user_id: int

class AccountUpdate(AccountBase):
    name: str | None = None
        