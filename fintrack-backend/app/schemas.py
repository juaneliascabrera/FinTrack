from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, model_validator


class UserBase(BaseModel):
    name: str | None = None


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
    model_config = ConfigDict(extra="forbid")


class AccountBase(BaseModel):
    name: str | None = None


class AccountPublic(AccountBase):
    name: str
    balance: int
    user_id: int


class AccountCreate(AccountBase):
    name: str
    balance: int


class AccountUpdate(AccountBase):
    name: str | None = None
    model_config = ConfigDict(extra="forbid")


# Transactions
class TransactionBase(BaseModel):
    amount: float
    description: str | None = None
    category: str | None = None
    type: TransactionType
    source_account: int
    destination_account: int | None = None
    timestamp: datetime | None = None


class TransactionCreate(TransactionBase):
    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_transfer_requirements(self) -> "TransactionCreate":
        if self.type == TransactionType.TRANSFER and self.destination_account is None:
            raise ValueError("Transfer needs a destination account.")
        if (
            self.type != TransactionType.TRANSFER
            and self.destination_account is not None
        ):
            raise ValueError("Only transfers can have a destination account.")
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero")
        return self


class TransactionPublic(TransactionBase):
    id: int
    timestamp: datetime
