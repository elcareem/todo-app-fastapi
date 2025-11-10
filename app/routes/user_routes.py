from fastapi import APIRouter, status
from db.database import SessionDep
from models.user_models import UserCreate
from controllers.user_controller import create_user, get_users

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user_route(user: UserCreate, session: SessionDep):
    return create_user(user, session)

@router.get("/users")
def get_users_route(session: SessionDep):
    return get_users(session)
