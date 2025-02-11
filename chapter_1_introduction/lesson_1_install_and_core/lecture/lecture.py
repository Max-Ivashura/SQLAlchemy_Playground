"""
Lesson 1: Установка и Core

Примеры работы с SQLAlchemy Core.
"""

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select

# Шаг 1: Создаем движок для подключения к базе данных
engine = create_engine('sqlite:///example.db', echo=True)

# Шаг 2: Создаем объект MetaData
metadata = MetaData()

# Шаг 3: Определяем таблицу
users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('age', Integer)
)

# Шаг 4: Создаем таблицу в базе данных
metadata.create_all(engine)

print("Таблица users успешно создана.")

# Шаг 5: Выполняем запрос SELECT
with engine.connect() as connection:
    # Выбираем все записи из таблицы users
    query = select(users_table)
    result = connection.execute(query)
    for row in result:
        print(row)

# Шаг 6: Добавляем запись в таблицу
with engine.connect() as connection:
    insert_stmt = users_table.insert().values(name="Alice", age=30)
    connection.execute(insert_stmt)
    connection.commit()

print("Запись успешно добавлена.")
