"""
Lesson 2: Создание таблиц в SQLAlchemy

Примеры создания таблиц с различными типами данных, ограничениями и индексами.
"""

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date, Boolean, Index

# Шаг 1: Создаем движок для подключения к базе данных
engine = create_engine('sqlite:///example.db', echo=True)

# Шаг 2: Создаем объект MetaData
metadata = MetaData()

# Шаг 3: Определяем таблицу users
users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('age', Integer),
    Column('is_active', Boolean, default=True),
    Column('created_at', Date)
)

# Шаг 4: Определяем таблицу products с индексом
products_table = Table(
    'products', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), unique=True, nullable=False),
    Column('price', Float),
    Column('quantity', Integer),
    Index('idx_name_price', 'name', 'price')  # Создаем составной индекс
)

# Шаг 5: Создаем таблицы в базе данных
metadata.create_all(engine)

print("Таблицы users и products успешно созданы.")