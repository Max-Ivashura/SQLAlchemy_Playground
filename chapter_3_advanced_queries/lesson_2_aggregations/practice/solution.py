from sqlalchemy import create_engine, Column, Integer, String, Float, func, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Шаг 1: Создаем базовый класс для моделей
Base = declarative_base()

# Таблица-связь для отношения "многие-ко-многим"
product_category = Table(
    'product_category', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)


# Определяем модель Product
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    price = Column(Float)
    quantity = Column(Integer)

    # Связь с Category через таблицу-связь
    categories = relationship('Category', secondary=product_category, back_populates='products')

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"


# Определяем модель Category
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    # Связь с Product через таблицу-связь
    products = relationship('Product', secondary=product_category, back_populates='categories')

    def __repr__(self):
        return f"<Category(name='{self.name}')>"


# Создаем движок
engine = create_engine('sqlite:///products.db', echo=True)

# Генерируем таблицы
Base.metadata.create_all(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Добавляем тестовые данные
phone = Product(name='phone 99 PRO', price=15.99, quantity=2)
pc = Product(name='pc MSI', price=150.99, quantity=3)
toaster = Product(name='toaster Pro Ultra Heat', price=1.99, quantity=2)
tv = Product(name='tv UltraWide 128K', price=30.99, quantity=2)

phone.categories = [Category(name='phone'), Category(name='smartphone')]
pc.categories = [Category(name='pc'), Category(name='computer')]
toaster.categories = [Category(name='toast'), Category(name='kitchen')]
tv.categories = [Category(name='tv'), Category(name='home'), Category(name='zombie')]

session.add_all([phone, pc, toaster, tv])
session.commit()

# COUNT: Подсчитываем общее количество продуктов
product_count = session.query(Product).count()
print("Продуктов:", product_count)

# SUM: Вычисляем общую стоимость всех продуктов
total_price = session.query(func.sum(Product.price * Product.quantity)).scalar()
print("Стоимость всех продуктов:", total_price)

# AVG: Вычисляем среднюю цену продукта
avg_price = session.query(func.avg(Product.price)).scalar()
print(f"Средняя стоимость продуктов: {avg_price:.2f}")

# MIN/MAX: Находим минимальную и максимальную цены
min_price = session.query(func.min(Product.price)).scalar()
max_price = session.query(func.max(Product.price)).scalar()
print(f"Min стоимость продуктов: {min_price:.2f}")
print(f"Max стоимость продуктов: {max_price:.2f}")

# ГРУППИРОВКА: Вычисляем общую стоимость продуктов по категориям
print("Стоимость продуктов по категориям:")
price_by_category = (
    session.query(Category.name, func.sum(Product.price * Product.quantity))
    .select_from(Product)
    .join(Product.categories)
    .group_by(Category.name)
    .all()
)
for category_name, price in price_by_category:
    print(f"{category_name}: {price:.2f}")
