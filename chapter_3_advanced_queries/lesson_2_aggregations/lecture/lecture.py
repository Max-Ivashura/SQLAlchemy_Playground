"""
Lesson 2: Агрегатные функции в SQLAlchemy

Примеры использования COUNT, SUM, AVG, MIN и MAX.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Шаг 1: Создаем базовый класс для моделей
Base = declarative_base()

# Шаг 2: Определяем модель Product
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float)
    quantity = Column(Integer)

    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price}, quantity={self.quantity})>"

# Шаг 3: Создаем движок и связываем его с базовым классом
engine = create_engine('sqlite:///example.db', echo=True)
Base.metadata.create_all(engine)

# Шаг 4: Создаем сессию для работы с данными
Session = sessionmaker(bind=engine)
session = Session()

# Добавляем тестовые данные
test_data = [
    Product(name="Phone", price=199.99, quantity=10),
    Product(name="Laptop", price=999.99, quantity=5),
    Product(name="TV", price=499.99, quantity=3),
    Product(name="Headphones", price=99.99, quantity=20),
]
session.add_all(test_data)
session.commit()

# COUNT: Подсчитываем количество продуктов
product_count = session.query(func.count(Product.id)).scalar()
print(f"Количество продуктов: {product_count}")

# SUM: Вычисляем общую стоимость всех продуктов
total_price = session.query(func.sum(Product.price * Product.quantity)).scalar()
print(f"Общая стоимость всех продуктов: {total_price:.2f}")

# AVG: Вычисляем среднюю цену продукта
average_price = session.query(func.avg(Product.price)).scalar()
print(f"Средняя цена продукта: {average_price:.2f}")

# MIN/MAX: Находим минимальную и максимальную цены
min_price = session.query(func.min(Product.price)).scalar()
max_price = session.query(func.max(Product.price)).scalar()
print(f"Минимальная цена: {min_price:.2f}, Максимальная цена: {max_price:.2f}")