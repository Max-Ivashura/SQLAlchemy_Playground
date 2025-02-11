"""
Lesson 1: Declarative Base в SQLAlchemy ORM

Примеры создания моделей данных с использованием Declarative Base.
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Шаг 1: Создаем базовый класс для моделей
Base = declarative_base()


# Шаг 2: Определяем модель User
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer)

    def __repr__(self):
        return f"<User(name={self.name}, age={self.age})>"


# Шаг 3: Создаем движок и связываем его с базовым классом
engine = create_engine('sqlite:///example.db', echo=True)
Base.metadata.create_all(engine)

# Шаг 4: Создаем сессию для работы с данными
Session = sessionmaker(bind=engine)
session = Session()

# Шаг 5: Добавляем запись в таблицу
new_user = User(name="Alice", age=30)
session.add(new_user)
session.commit()

# Шаг 6: Выбираем все записи из таблицы
users = session.query(User).all()
for user in users:
    print(user)

print("Таблица users успешно создана, данные добавлены.")
