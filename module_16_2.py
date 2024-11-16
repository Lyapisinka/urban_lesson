from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()


@app.get("/")
async def read_main():
    return {"message": "Главная страница"}


@app.get("/user/admin")
async def read_admin():
    return {"message": "Вы вошли как администратор"}


@app.get("/user/{user_id}")
async def read_user(user_id: Annotated[int, Path(title="Enter User ID",
                                                 ge=1,
                                                 le=100,
                                                 description="Идентификатор пользователя должен быть целым числом и "
                                                             "находиться в диапазоне от 1 до 100.",
                                                 example=1)]):
    return {"message": f"Вы вошли как пользователь № {user_id}"}


@app.get("/user/{username}/{age}")
async def read_user_info(username: Annotated[str, Path(title="Enter username",
                                                       min_length=5,
                                                       max_length=20,
                                                       description="Имя пользователя должно быть строкой длиной от 5 "
                                                                   "до 20 символов.",
                                                       example="UrbanUser")], age: Annotated[
    int, Path(title="Enter age",
              ge=18,
              le=120,
              description="Возраст пользователя должен быть целым числом и находиться в диапазоне от 18 до 120.",
              example=24)]):
    return {"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"}
