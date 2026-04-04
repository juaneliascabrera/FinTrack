from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index = True)
    email: str
    password: str
    