from pydantic import BaseModel
from typing import Optional

class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int

    class Config:
        orm_mode = True

class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int

class CreateTask(BaseModel):
    title: str
    content: str
    priority: int
    completed: bool

    class Config:
        orm_mode = True

class UpdateTask(BaseModel):
    title: str
    content: str
    priority: int
