"""
Lesson 3: Подзапросы (Subqueries) в SQLAlchemy

Примеры использования подзапросов для выполнения сложных запросов.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, select, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased

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

# ПОДЗАПРОС: Находим продукты с ценой выше средней
average_price_query = (
    select(func.avg(Product.price).label("average_price"))
)
average_price = session.execute(average_price_query).scalar()

expensive_products = (
    session.query(Product)
    .filter(Product.price > average_price)
    .all()
)

print(f"Средняя цена: {average_price:.2f}")
print("Продукты с ценой выше средней:")
for product in expensive_products:
    print(product)

# ПОДЗАПРОС: Используем алиас для самосоединения
ProductAlias = aliased(Product)

cross_products = (
    session.query(Product.name.label("product_name"), ProductAlias.name.label("alias_name"))
    .join(ProductAlias, Product.price > ProductAlias.price)
    .all()
)

print("Продукты с ценой выше других:")
for product in cross_products:
    print(f"{product.product_name} > {product.alias_name}")