from sqlalchemy import create_engine, Column, Integer, String, Float, select, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased

# Шаг 1: Создаем базовый класс для моделей
Base = declarative_base()

# Шаг 2: Определяем модель Product и Category
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float)
    quantity = Column(Integer)
    category_id = Column(Integer, ForeignKey('categories.id'))

    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price}, quantity={self.quantity})>"

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Category(name={self.name})>"

# Шаг 3: Создаем движок и связываем его с базовым классом
engine = create_engine('sqlite:///products.db', echo=True)
Base.metadata.create_all(engine)

# Шаг 4: Создаем сессию для работы с данными
Session = sessionmaker(bind=engine)
session = Session()

# Добавляем тестовые данные
electronics = Category(name="Electronics")
other = Category(name="Other")

test_data = [
    Product(name="Phone", price=199.99, quantity=10, category_id=electronics.id),
    Product(name="Laptop", price=999.99, quantity=5, category_id=electronics.id),
    Product(name="TV", price=499.99, quantity=3, category_id=electronics.id),
    Product(name="Headphones", price=99.99, quantity=20, category_id=other.id),
]
session.add(electronics)
session.add(other)
session.add_all(test_data)
session.commit()

# ЗАДАНИЕ 1: Продукты с ценой выше максимальной в категории "Electronics"
max_price_in_electronics_query = (
    select(func.max(Product.price)).where(Product.category_id == electronics.id)
).scalar_subquery()  # Используем .scalar_subquery()

expensive_products = (
    session.query(Product)
    .filter(Product.price > max_price_in_electronics_query)
    .all()
)

print("Продукты с ценой выше максимальной в категории Electronics:")
for product in expensive_products:
    print(product)

# ЗАДАНИЕ 2: Самосоединение для сравнения цен
ProductAlias = aliased(Product)

cross_products = (
    session.query(Product.name.label("product_name"), ProductAlias.name.label("alias_name"))
    .join(ProductAlias, Product.price > ProductAlias.price)
    .all()
)

print("Пары продуктов, где цена первого продукта больше цены второго:")
for pair in cross_products:
    print(f"{pair.product_name} > {pair.alias_name}")

# ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: Фильтрация продуктов по минимальному количеству на складе
min_quantity_query = (
    select(func.min(Product.quantity))
).scalar_subquery()  # Используем .scalar_subquery()

filtered_products = (
    session.query(Product)
    .filter(Product.quantity >= min_quantity_query)
    .all()
)

print(f"Продукты с количеством не менее минимального:")
for product in filtered_products:
    print(product)