"""
Lesson 3: Базовые запросы в SQLAlchemy ORM

Примеры выполнения фильтрации, сортировки и ограничения результатов.
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

# Добавляем несколько записей для тестирования
users_data = [
    User(name="Alice", age=30),
    User(name="Bob", age=25),
    User(name="Charlie", age=35),
]
session.add_all(users_data)
session.commit()

# ФИЛЬТРАЦИЯ: Выбираем пользователей старше 30 лет
filtered_users = session.query(User).filter(User.age > 30).all()
print("Пользователи старше 30 лет:")
for user in filtered_users:
    print(user)

# СОРТИРОВКА: Выбираем пользователей, отсортированных по возрасту
sorted_users = session.query(User).order_by(User.age.desc()).all()
print("Пользователи, отсортированные по возрасту (по убыванию):")
for user in sorted_users:
    print(user)

# ОГРАНИЧЕНИЕ: Выбираем только первые две записи
limited_users = session.query(User).limit(2).all()
print("Первые два пользователя:")
for user in limited_users:
    print(user)