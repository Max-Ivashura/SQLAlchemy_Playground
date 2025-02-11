from sqlalchemy import Column, VARCHAR, Float, Integer, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Создаем базовый класс для моделей
Base = declarative_base()

# Определяем модель Product
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100), unique=True)
    price = Column(Float)
    quantity = Column(Integer)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, quantity={self.quantity})>"

# Создаем движок
engine = create_engine('sqlite:///products.db')

# Генерируем таблицу на основе модели
Base.metadata.create_all(engine)

# Создаем фабрику сессий
Session = sessionmaker(bind=engine)
session = Session()

# Добавляем записи в таблицу
products_to_add = [
    Product(name='Phone', price=199.99, quantity=10),
    Product(name='Phone 2', price=199.99, quantity=10),
    Product(name='TV', price=999.99, quantity=5),
    Product(name='PC', price=4999.99, quantity=1),
    Product(name='GPU', price=1999.99, quantity=3),
]

# Проверяем наличие записи перед добавлением
for product in products_to_add:
    existing_product = session.query(Product).filter_by(name=product.name).first()
    if not existing_product:
        session.add(product)
session.commit()

# ФИЛЬТРАЦИЯ: Выбираем продукты с ценой больше 200
print("Товары с ценой больше 200")
products_price_200 = session.query(Product).filter(Product.price > 200).all()
for product in products_price_200:
    print(product)

# СОРТИРОВКА: Выбираем продукты, отсортированные по цене (по возрастанию)
print("Товары с ценой по возрастанию")
products_sorted = session.query(Product).order_by(Product.price).all()
for product in products_sorted:
    print(product)

# ОГРАНИЧЕНИЕ: Выбираем первые три продукта
print("Первые 3 товара в таблице")
products_top_3 = session.query(Product).limit(3).all()
for product in products_top_3:
    print(product)

# ПОИСК: Находим продукты, где имя содержит подстроку "Phone"
print("Товары содержат Phone")
products_phone = session.query(Product).filter(Product.name.contains("Phone")).all()
for product in products_phone:
    print(product)