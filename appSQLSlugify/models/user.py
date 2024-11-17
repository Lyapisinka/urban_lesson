from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from appSQLSlugify.backend.db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    tasks = relationship("Task", back_populates="user")




from sqlalchemy.schema import CreateTable
print(CreateTable(User.__table__))