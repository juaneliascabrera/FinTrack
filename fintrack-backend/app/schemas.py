from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    name: str | None = None
    
class UserCreate(UserBase):
    name: str