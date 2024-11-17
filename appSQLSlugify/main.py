from fastapi import FastAPI
from appSQLSlugify.routers import user, task
from appSQLSlugify.backend.db import engine, Base

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(task.router, prefix="/tasks", tags=["tasks"])