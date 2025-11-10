from fastapi import FastAPI
from sqlmodel import SQLModel
from db.database import engine
from routes.user_routes import router as user_router
from routes.todo_routes import router as todo_router

app = FastAPI(title="Todo App")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(user_router)
app.include_router(todo_router)
