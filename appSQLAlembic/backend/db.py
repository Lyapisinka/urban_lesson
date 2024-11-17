from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Создание движка для подключения к базе данных
DATABASE_URL = "sqlite:///taskAlembic.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создание сессии для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех ORM моделей
Base = declarative_base()