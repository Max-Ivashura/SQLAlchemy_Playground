"""
Lesson 1: Объединения (Joins) в SQLAlchemy

Примеры выполнения различных типов JOIN с использованием SQLAlchemy ORM.
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Шаг 1: Создаем базовый класс для моделей
Base = declarative_base()

# Шаг 2: Определяем модели User и Address
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    # Связь с Address
    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"<User(name={self.name})>"

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Связь с User
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"<Address(email={self.email})>"

# Шаг 3: Создаем движок и связываем его с базовым классом
engine = create_engine('sqlite:///example.db', echo=True)
Base.metadata.create_all(engine)

# Шаг 4: Создаем сессию для работы с данными
Session = sessionmaker(bind=engine)
session = Session()

# Добавляем тестовые данные
alice = User(name="Alice")
bob = User(name="Bob")

alice.addresses = [Address(email="alice@example.com"), Address(email="a.nother@example.com")]
bob.addresses = [Address(email="bob@example.com")]

session.add_all([alice, bob])
session.commit()

# INNER JOIN: Выбираем пользователей и их адреса
inner_join_results = session.query(User, Address).join(Address).all()
print("INNER JOIN:")
for user, address in inner_join_results:
    print(f"{user.name} -> {address.email}")

# LEFT JOIN: Выбираем всех пользователей и их адреса (даже если адреса отсутствуют)
left_join_results = session.query(User, Address).outerjoin(Address).all()
print("LEFT JOIN:")
for user, address in left_join_results:
    print(f"{user.name} -> {address.email if address else 'No address'}")