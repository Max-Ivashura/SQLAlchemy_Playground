"""
Lesson 2: Работа с сессиями и CRUD-операциями в SQLAlchemy ORM

Примеры выполнения CRUD-операций через сессии.
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

# CREATE: Добавляем запись
new_user = User(name="Alice", age=30)
session.add(new_user)
session.commit()
print("Запись успешно добавлена.")

# READ: Выбираем все записи
users = session.query(User).all()
for user in users:
    print(user)

# UPDATE: Обновляем запись
user_to_update = session.query(User).filter_by(name="Alice").first()
if user_to_update:
    user_to_update.age = 31
    session.commit()
    print("Запись успешно обновлена.")

# DELETE: Удаляем запись
user_to_delete = session.query(User).filter_by(name="Alice").first()
if user_to_delete:
    session.delete(user_to_delete)
    session.commit()
    print("Запись успешно удалена.")