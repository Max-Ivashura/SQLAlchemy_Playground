"""
Lesson 3: Соединения с базой данных в SQLAlchemy

Примеры создания движков для разных СУБД и выполнения CRUD-операций.
"""

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert, select, update, delete

# Шаг 1: Создаем движок для SQLite
sqlite_engine = create_engine('sqlite:///example.db', echo=True)

# Шаг 2: Создаем движок для PostgreSQL (замените на ваши данные)
# postgres_engine = create_engine('postgresql://username:password@localhost/mydatabase', echo=True)

# Шаг 3: Создаем движок для MySQL (замените на ваши данные)
# mysql_engine = create_engine('mysql+pymysql://username:password@localhost/mydatabase', echo=True)

# Шаг 4: Создаем таблицу users
metadata = MetaData()
users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('age', Integer)
)

# Шаг 5: Создаем таблицу в базе данных
metadata.create_all(sqlite_engine)

# Шаг 6: Выполняем CRUD-операции

# CREATE: Добавляем запись
with sqlite_engine.connect() as connection:
    insert_stmt = insert(users_table).values(name="Alice", age=30)
    connection.execute(insert_stmt)

# READ: Выбираем все записи
with sqlite_engine.connect() as connection:
    query = select(users_table)
    result = connection.execute(query)
    for row in result:
        print(row)

# UPDATE: Обновляем запись
with sqlite_engine.connect() as connection:
    update_stmt = update(users_table).where(users_table.c.id == 1).values(age=31)
    connection.execute(update_stmt)

# DELETE: Удаляем запись
with sqlite_engine.connect() as connection:
    delete_stmt = delete(users_table).where(users_table.c.id == 1)
    connection.execute(delete_stmt)

print("CRUD-операции успешно выполнены.")
