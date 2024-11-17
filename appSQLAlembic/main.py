from sqlalchemy import MetaData
from sqlalchemy.schema import CreateTable

from backend.db import engine, Base

# Для отображения SQL создания таблиц
metadata = MetaData()


def print_create_tables():
    for table in Base.metadata.sorted_tables:
        print(CreateTable(table).compile(engine))


print_create_tables()