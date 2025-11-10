from fastapi import HTTPException, status
from sqlmodel import select
from models.todo_models import TodoInDb, TodoCreate
from models.user_models import UserInDb
from db.database import SessionDep

def create_todo(todo: TodoCreate, session: SessionDep):
    user = session.get(UserInDb, todo.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if not todo.user_id or not todo.title or not todo.description:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="All fields are required"
        )
    
    new_todo = TodoInDb(
        **todo.model_dump(),
        created_at=None,
        updated_at=None
    )
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    
    return {
        "success": True,
        "data": new_todo,
        "detail": "Users retrieved successfully"
    }

def get_todos(session: SessionDep):
    todos = session.exec(select(TodoInDb)).all()

    if not todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No available todo"
        )
    
    return {
        "success": True,
        "data": todos,
        "detail": "Users retrieved successfully"
    }

def get_user_todos(user_id: int, session: SessionDep):
    user = session.get(UserInDb, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    todos = session.exec(select(TodoInDb).where(TodoInDb.user_id == user_id)).all()
    if not todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No available todo"
        )
    
    return {
        "success": True,
        "data": todos,
        "detail": "Todos retrieved successfully"
    }