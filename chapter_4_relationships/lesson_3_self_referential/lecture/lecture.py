"""
Lesson 3: Селф-референциальные отношения в SQLAlchemy

Примеры определения и использования селф-референциальных отношений.
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Шаг 1: Создаем базовый класс для моделей
Base = declarative_base()

# Шаг 2: Определяем модель Employee с селф-референциальным отношением
class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    manager_id = Column(Integer, ForeignKey('employees.id'))

    # Связь с самой собой
    manager = relationship('Employee', remote_side=[id], back_populates='subordinates')
    subordinates = relationship('Employee', back_populates='manager')

    def __repr__(self):
        return f"<Employee(name={self.name}, manager={self.manager.name if self.manager else None})>"

# Шаг 3: Создаем движок и связываем его с базовым классом
engine = create_engine('sqlite:///example.db', echo=True)
Base.metadata.create_all(engine)

# Шаг 4: Создаем сессию для работы с данными
Session = sessionmaker(bind=engine)
session = Session()

# Добавляем тестовые данные
alice = Employee(name="Alice")  # Менеджер
bob = Employee(name="Bob", manager=alice)  # Подчиненный Alice
charlie = Employee(name="Charlie", manager=alice)  # Подчиненный Alice

session.add_all([alice, bob, charlie])
session.commit()

# Запросы с использованием селф-референциального отношения
print("Сотрудники и их менеджеры:")
for employee in session.query(Employee).all():
    print(f"{employee.name}:")
    if employee.manager:
        print(f"  - Менеджер: {employee.manager.name}")
    else:
        print("  - Менеджер: Нет")

print("\nМенеджеры и их подчиненные:")
for employee in session.query(Employee).all():
    if employee.subordinates:
        print(f"{employee.name} управляет следующими сотрудниками:")
        for subordinate in employee.subordinates:
            print(f"  - {subordinate.name}")
    else:
        print(f"{employee.name} не управляет никем.")