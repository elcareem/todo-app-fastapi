from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from models.user_models import UserInDb, UserCreate, UserResponse
from db.database import SessionDep

def create_user(user: UserCreate, session: SessionDep):
    
    existing_user = session.exec(select(UserInDb).where(UserInDb.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )
    
    if not user.username or not user.password or not user.email:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="All fields are required"
        )

    new_user = UserInDb(
        **user.model_dump(),
        created_at=None,
        updated_at=None
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    created_user = UserResponse.from_orm(new_user)

    return {
        "success": True,
        "data": created_user,
        "detail": "User created successfully"
    }

def get_users(session: SessionDep):
    users = session.exec(select(UserInDb)).all()
    retrieved_users = [UserResponse.from_orm(user) for user in users]

    if not retrieved_users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No available users"
        )

    return {
        "success": True,
        "data": retrieved_users,
        "detail": "Users retrieved successfully"
    }
