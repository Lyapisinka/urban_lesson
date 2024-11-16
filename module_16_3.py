from fastapi import FastAPI, HTTPException, Path
from typing import Annotated, Dict

app = FastAPI()

# Инициализируем словарь пользователей
users: Dict[str, str] = {'1': 'Имя: Example, возраст: 18'}


@app.get("/users")
async def get_users():
    return users


@app.post("/user/{username}/{age}")
async def add_user(username: Annotated[str, Path(title="Enter username",
                                                 min_length=5,
                                                 max_length=20,
                                                 description="Имя пользователя должно быть строкой длиной от 5 до 20 символов.",
                                                 example="UrbanUser")], age: Annotated[int, Path(title="Enter age",
                                                                                                 ge=18,
                                                                                                 le=120,
                                                                                                 description="Возраст пользователя должен быть целым числом и находиться в диапазоне от 18 до 120.",
                                                                                                 example=24)]):
    new_id = str(max(map(int, users.keys())) + 1)
    users[new_id] = f"Имя: {username}, возраст: {age}"
    return {"message": f"User {new_id} is registered"}


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: Annotated[str, Path(title="Enter User ID", description="Идентификатор пользователя.", example="1")],
        username: Annotated[str, Path(title="Enter username",
                                      min_length=5,
                                      max_length=20,
                                      description="Имя пользователя должно быть строкой длиной от 5 до 20 символов.",
                                      example="UrbanProfi")], age: Annotated[int, Path(title="Enter age",
                                                                                       ge=18,
                                                                                       le=120,
                                                                                       description="Возраст пользователя должен быть целым числом и находиться в диапазоне от 18 до 120.",
                                                                                       example=28)]):
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return {"message": f"The user {user_id} is updated"}


@app.delete("/user/{user_id}")
async def delete_user(
        user_id: Annotated[str, Path(title="Enter User ID", description="Идентификатор пользователя.", example="2")]):
    del users[user_id]
    return {"message": f"User {user_id} is deleted"}
