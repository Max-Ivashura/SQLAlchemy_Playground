"""
Lesson 2: Отношения "многие-ко-многим" в SQLAlchemy

Примеры определения и использования отношений "многие-ко-многим".
"""

from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Шаг 1: Создаем базовый класс для моделей
Base = declarative_base()

# Шаг 2: Создаем промежуточную таблицу для Many-to-Many
product_category = Table(
    'product_category', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

# Шаг 3: Определяем модели Product и Category
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)

    # Связь с Category через промежуточную таблицу
    categories = relationship('Category',
                              secondary=product_category, back_populates='products')

    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price})>"

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    # Связь с Product через промежуточную таблицу
    products = relationship('Product',
                            secondary=product_category, back_populates='categories')

    def __repr__(self):
        return f"<Category(name={self.name})>"

# Шаг 4: Создаем движок и связываем его с базовым классом
engine = create_engine('sqlite:///example.db', echo=True)
Base.metadata.create_all(engine)

# Шаг 5: Создаем сессию для работы с данными
Session = sessionmaker(bind=engine)
session = Session()

# Добавляем тестовые данные
phone = Product(name="Phone", price=199.99)
laptop = Product(name="Laptop", price=999.99)

electronics = Category(name="Electronics")
gadgets = Category(name="Gadgets")

phone.categories = [electronics, gadgets]
laptop.categories = [electronics]

session.add_all([phone, laptop, electronics, gadgets])
session.commit()

# Запросы с использованием отношений
print("Продукты и их категории:")
for product in session.query(Product).all():
    print(f"{product.name}:")
    for category in product.categories:
        print(f"  - {category.name}")

print("\nКатегории и их продукты:")
for category in session.query(Category).all():
    print(f"{category.name}:")
    for product in category.products:
        print(f"  - {product.name}")