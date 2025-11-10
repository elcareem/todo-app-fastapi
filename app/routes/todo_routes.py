from fastapi import APIRouter, status
from db.database import SessionDep
from models.todo_models import TodoCreate
from controllers.todo_controller import create_todo, get_todos, get_user_todos

router = APIRouter()

@router.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo_route(todo: TodoCreate, session: SessionDep):
    return create_todo(todo, session)

@router.get("/todos")
def get_todos_route(session: SessionDep):
    return get_todos(session)

@router.get("/todos/{user_id}")
def get_user_todos_route(user_id: int, session: SessionDep):
    return get_user_todos(user_id, session)
