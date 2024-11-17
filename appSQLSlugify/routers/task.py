from fastapi import APIRouter, Depends, HTTPException, status
from slugify import slugify
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from typing import List, Annotated

from appSQLSlugify.schemas import CreateTask, UpdateTask
from appSQLSlugify.backend.db_depends import get_db
from appSQLSlugify.models import Task as TaskModel
from appSQLSlugify.models import User as UserModel

router = APIRouter()

@router.get("/", response_model=List[CreateTask])
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.execute(select(TaskModel)).scalars().all()
    return [CreateTask.from_orm(task) for task in tasks]


@router.get("/{task_id}", response_model=CreateTask)
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.get(TaskModel, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return CreateTask.from_orm(task)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_task(task_data: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    print(f"Attempting to find user with ID: {user_id}")
    user = db.get(UserModel, user_id)
    if user is None:
        print("No user found.")
        raise HTTPException(status_code=404, detail="User was not found")

    print(f"Found user: {user}")
    slug_task = slugify(task_data.title.lower())
    new_task = TaskModel(title=task_data.title,
                         content=task_data.content,
                         priority=task_data.priority,
                         user_id=user.id,
                         completed=task_data.completed,
                         slug=slug_task)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.put("/update/{task_id}", response_model=CreateTask)
async def update_task(task_id: int, task_data: CreateTask, db: Annotated[Session, Depends(get_db)]):
    task = db.get(TaskModel, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = task_data.title
    task.description = task_data.content
    db.commit()
    db.refresh(task)
    return CreateTask.from_orm(task)


@router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.get(TaskModel, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()


