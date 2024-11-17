from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from typing import Annotated, List
from appSQLSlugify.models import User as UserModel  # Переименование SQLAlchemy модели для ясности
from appSQLSlugify.schemas import CreateUser, UpdateUser, CreateTask, UpdateTask# Импортируем Pydantic схемы
from slugify import slugify
from appSQLSlugify.backend.db_depends import get_db
from appSQLSlugify.models import Task as TaskModel
router = APIRouter()


# Маршрут для получения всех пользователей
@router.get("/", response_model=List[CreateUser])  # Используем CreateUser или создаем отдельную схему для просмотра
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(UserModel)).scalars().all()
    return [CreateUser.from_orm(user) for user in users]


# Маршрут для получения пользователя по ID
@router.get("/{user_id}", response_model=CreateUser)  # Используем CreateUser или создаем отдельную схему для просмотра
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(UserModel).where(UserModel.id == user_id)).scalar_one_or_none()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User was not found")

@router.get("/{user_id}/tasks", response_model=List[CreateTask])
async def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    tasks = db.execute(select(TaskModel).where(TaskModel.user_id == user_id)).scalars().all()
    return [CreateTask.from_orm(task) for task in tasks]

# Маршрут для создания нового пользователя
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: CreateUser, db: Annotated[Session, Depends(get_db)]):
    slug_user= slugify(user_data.username)
    new_user = UserModel(username=user_data.username,
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        age=user_data.age,
        slug=slug_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


# Маршрут для обновления пользователя
@router.put("/update/{user_id}")
async def update_user(user_id: int, user_data: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(UserModel).where(UserModel.id == user_id)).scalar_one_or_none()
    if user:
        db.execute(update(UserModel).where(UserModel.id == user_id).values(firstname=user_data.firstname,
            lastname=user_data.lastname,
            age=user_data.age))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
    raise HTTPException(status_code=404, detail="User was not found")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Удаление связанных задач
    tasks = db.execute(select(TaskModel).where(TaskModel.user_id == user_id)).scalars().all()
    for task in tasks:
        db.delete(task)

    # Удаление пользователя
    db.delete(user)
    db.commit()