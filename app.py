from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum

app = FastAPI(title="Todo list")

class SortOrder(Enum):
    ascending = "ascending"
    descending = "descending"

class User(BaseModel):
    username: str
class UserCreate(User):
    password: str
class UserInDb(UserCreate):
    created_at: datetime
    updated_at: datetime
class UserResponse(User):
    created_at: datetime
    updated_at: datetime

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskinDb(TaskCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    is_completed: bool 

class TaskUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None

class Database:
    def __init__(self):
        # two tables
        self._users: Dict[int,UserInDb] = {}
        self._task: Dict[int, List[TaskinDb]]= {}
        self.id_task= 1
        self.user_id = 1

    def add_task(self, user_id:int, task:TaskinDb):

        self._task.setdefault(user_id, []).append(task)
    
    def get_tasks(self):
        return self._task

    def get_user_tasks(self, user_id: int):
        if user_id in self._task:
            return self._task[user_id]

    def sort_tasks(self, sort:SortOrder):
        
        sorted_task = []
        tasks_title = {}
        for tasks in self._task.values():
            for task in tasks:
                tasks_title.update({task.title: task})
        
        if sort.value == "ascending":
            titles = tasks_title.keys()
            titles = list(titles)
            titles = sorted(titles)
            print(titles)
        elif sort.value == "descending":
            titles = tasks_title.keys()
            titles = list(titles)
            titles = sorted(titles)
            print(titles)

        for title in titles:
            sorted_task.append(tasks_title[title])

        return sorted_task
        
        
            

    def update_user_task_by_id(self, user_id: int, task_to_update: TaskUpdate):
        
        user_tasks = self.get_user_tasks(user_id)
        for i, user_task in enumerate(user_tasks):
            if user_task.id == task_to_update.id:

                task_to_update = task_to_update.model_dump(exclude_unset=True)
                user_task = user_task.model_dump()
                user_task.update(task_to_update)

                updated_task = TaskinDb(**user_task)
                self._task[user_id][i] = updated_task
                return updated_task
            
    def update_user_task_by_username(self, username: str, task_to_update: TaskUpdate):

        for user_id, user_detail in self._users.items():
            if user_detail.username == username:
                updated_task = self.update_user_task_by_id(user_id, task_to_update)
                return updated_task

    def delete_task(self, task_id: int):
        for user_id, tasks in self._task.items():
            for task in tasks:
                if task.id == task_id:
                    removed_task = tasks.pop(tasks.index(task))
                    if not db_instance._task[user_id]:
                        db_instance._task.pop(user_id)

                    return removed_task

    def increment_id_task(self):
        self.id_task+= 1
    def increment_id_user(self):
        self.user_id += 1

    # user method

    def add_user(self, user: UserInDb) -> UserInDb | None:
        for _, user_details in self._users.items():
            print("User Details", user_details)
            print("User", user)
            if user_details.username == user.username:
                return None
        user_id= self.user_id
        self._users[user_id] = user
        self.increment_id_user()
        return user
    
    def get_all_users(self):
        return self._users
    
    def check_user(self, user_id:int):
        if not user_id in self._users:
            return None
        return user_id
    
    def delete_user(self, user_id: int):
        if user_id in self._users:
            deleted_user = self._users.pop(user_id)
            if user_id in self._task:
                self._task.pop(user_id)
            
            return deleted_user
        

db_instance = Database()

# Endpoints

@app.get("/")
def index():
    return{
        "message": "Todo App"
    }

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, user_id: int):
    if not task.title or not task.description:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="All fields are required"
        )
    user_id = db_instance.check_user(user_id)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    

    new_task = TaskinDb(
        title=task.title,
        description= task.description,
        id =db_instance.id_task,
        created_at= datetime.utcnow(),
        updated_at=datetime.utcnow(),
        is_completed=False
    )
    db_instance.increment_id_task()
    db_instance.add_task(user_id=user_id, task=new_task)

    return {
        "success": True,
        "data": new_task,
        "message": "Task created successfully"
    }

@app.get("/tasks")
def get_user_tasks(id:int = None, search: str = None, sort: SortOrder = None):

    if id:
        user_id = db_instance.check_user(id)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exist"
            )
        user_tasks= None
        for id_in_db, user_task in db_instance._task.items():
            if id_in_db == id:
                user_tasks = user_task
        return {
            "success": True,
            "data": user_tasks,
            "message": "All User tasks retrieved successfully"
        }
    
    if search:
        found = []

        for tasks in db_instance._task.values():
            for task in tasks:
                user_task = task.model_dump()
                if search in user_task["title"] or search in user_task["description"]:
                    found.append(task)
        if found:
            return {
                "success": True,
                "data" : found,
                "message": "Word match successful"
            }

    
    if sort:
        return db_instance.sort_tasks(sort)
        

    tasks =  db_instance.get_tasks()
    return{
       "success": True,
       "data": tasks,
       "message": "All tasks retrieved successfully"
    }

@app.patch("/tasks")
def update_user_task_by_id(user_id: int, task: TaskUpdate):
    # todo

    if user_id not in db_instance._users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not task.title and not task.description:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="At least one field is required"
        )
    
    updated_task = db_instance.update_user_task_by_id(user_id, task)
    
    if updated_task:
        return {
            "success": True,
            "data": updated_task,
            "message": "Task updated successfully"
        }

@app.patch("/tasks")
def update_user_task_by_username(user_name: str, task: TaskUpdate):
    # todo
    found = False
    for user_detail in db_instance._users.values():
            if user_detail.username == user_name:
                print(user_detail)
                found = True
    
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not task.title and not task.description:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="At least one field is required"
        )
    
    updated_task = db_instance.update_user_task_by_username(user_name, task)

    if updated_task:
        return {
            "success": True,
            "data": updated_task,
            "message": "Task updated successfully"
        }

@app.delete("/tasks")
def delete_task(id: int):

    deleted_task = db_instance.delete_task(id)

    if not deleted_task:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )
        
    return {
        "success": True,
        "data": deleted_task,
        "message": "Task deleted successfully"
    }
    
#============================
# User endpoints

@app.post("/users")
def register_user(user: UserCreate):
    if not  user.username or     not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All Fields are required"
        )
    new_user = UserInDb(
        **user.model_dump(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()                   
    )
    user = db_instance.add_user(new_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist"
        )
    return {
        "success": True,
        "data": UserResponse(**user.model_dump(exclude_unset=True)),
        "message": "User created Successfully"
    }
   
@app.get("/users")
def get_users():
    users = db_instance.get_all_users()
    return {
        "success": True,
        "data": users,
         "message": "All Users retrived  Successfully"
    }
                
@app.delete("/users")
def delete_user(id: int):

    deleted_user = db_instance.delete_user(id)

    if not deleted_user:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

    return {
        "success": True,
        "data": deleted_user,
        "message": "User deleted successfully"
    }


   