from fastapi import FastAPI, Path, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


# Создаем экземпляр приложения FastAPI

app = FastAPI()
templates = Jinja2Templates(directory="templates")
users = []

class User(BaseModel):
    id: int
    username: str
    age: int


# Маршруты

@app.get("/", response_class=HTMLResponse)
async def get_tasks(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_all_users(request: Request, user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})

@app.post("/user/{username}/{age}", response_model=User)
async def create_user(username: Annotated[str, Path(min_length=3, max_length=20,
                                                 description='Enter user name', example='UrbanUser')],
                   age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]) -> User:
    user_id = max((t.id for t in users), default=0) + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}")
async def update_user( user_id: Annotated[int, Path(ge=1, le=150, description='Enter user ID', example=1)],
                       username: Annotated[str, Path(min_length=3, max_length=20,
                                                     description='Enter user name', example='UrbanUser')],
                       age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]):
        for u in users:
            if u.id == user_id:
                u.username = username
                u.age = age
        return u
        raise HTTPException(status_code=404, detail="Пользователь не найден")



@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(ge=1, le=150, description='Enter user ID', example=1)]):
    for i, t in enumerate(users):
        if t.id == user_id:
            del users[i]
    return {"Пользователь удален"}
    raise HTTPException(status_code=404, detail="Задача не найдена")






