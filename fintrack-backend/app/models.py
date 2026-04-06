from sqlalchemy.orm import foreign
from datetime import datetime, timezone
from typing import List

from sqlmodel import Field, Relationship, SQLModel

class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"    

class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    balance: float
    user: "User" = Relationship(back_populates="accounts")
    user_id: int = Field(foreign_key="user.id", index=True)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password: str
    accounts: List[Account] = Relationship(back_populates="user")

class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: float
    description: str | None = None
    category: str | None = None
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))
    from_account_id: int = Field(foreign_key="account.id", index=True)
    to_account_id: int | None = Field(default=None, foreign_key="account.id", index=True)
    type: TransactionType
     
