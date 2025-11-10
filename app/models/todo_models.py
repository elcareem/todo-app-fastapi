from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class TodoCreate(SQLModel):
    user_id: int = Field(foreign_key="users.id")
    title: str
    description: str

class TodoInDb(TodoCreate, table=True):
    __tablename__ = "todos"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_completed: bool = Field(default=False)

class TodoUpdate(SQLModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
