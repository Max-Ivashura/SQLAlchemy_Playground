from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, Boolean, Index

# Создаем движок с отображением SQL-запросов для отладки
engine = create_engine('sqlite:///solution.db', echo=True)

# Создаем объект MetaData
metadata = MetaData()

# Определяем таблицу employees
employees_table = Table(
    'employees', metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String(50), nullable=False),
    Column('last_name', String(100), nullable=False),
    Column('email', String(100), unique=True, nullable=False),
    Column('salary', Float),
    Column('hire_date', DateTime),
    Column('is_manager', Boolean, default=False),
    Index('idx_email', 'email'),  # Явно создаем индекс для email
    Index('idx_name', 'last_name', 'first_name')  # Составной индекс
)

# Создаем таблицу в базе данных
metadata.create_all(engine)

print("Таблица employees успешно создана.")
