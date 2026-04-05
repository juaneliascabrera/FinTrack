from sqlmodel import SQLModel, Field, Relationship
from typing import List
class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index = True)
    balance: int
    user: "User" = Relationship(back_populates="accounts")
    user_id: int = Field(foreign_key="user.id", index=True)
    
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str 
    email: str = Field(unique = True, index = True)
    password: str
    accounts: List[Account] = Relationship(back_populates="user")

