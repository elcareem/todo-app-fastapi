from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel):
    username: str
    email: str

class UserCreate(User):
    password: str

class UserInDb(UserCreate, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserResponse(User):
    id: int
    email: str
    created_at: datetime
    updated_at: datetime
