from sqlalchemy import Column, Float, Integer, String, Table, create_engine, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Создаем базовый класс для моделей
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
phone = Product(name='phone 99 PRO', price=15.99)
pc = Product(name='pc MSI', price=150.99)
toaster = Product(name='toaster Pro Ultra Heat', price=1.99)
tv = Product(name='tv UltraWide 128K', price=30.99)

phone.categories = [Category(name='phone'), Category(name='smartphone')]
pc.categories = [Category(name='pc'), Category(name='computer')]
toaster.categories = [Category(name='toast'), Category(name='kitchen')]
tv.categories = [Category(name='tv'), Category(name='home'), Category(name='zombie')]

session.add_all([phone, pc, toaster, tv])
session.commit()

# INNER JOIN: Выбираем продукты вместе с их категориями
print("INNER JOIN:")
inner_join_results = (
    session.query(Product, Category)
    .select_from(Product)  # Явно указываем основную таблицу
    .join(Product.categories)  # Указываем отношение для JOIN
    .all()
)
for product, category in inner_join_results:
    print(f"{product.name} -> {category.name}")

# LEFT JOIN: Выбираем все продукты, даже если у них нет категории
print("LEFT JOIN:")
left_join_results = (
    session.query(Product, Category)
    .select_from(Product)  # Явно указываем основную таблицу
    .outerjoin(Product.categories)  # Указываем отношение для OUTER JOIN
    .all()
)
for product, category in left_join_results:
    print(f"{product.name} -> {category.name if category else 'No category'}")

# ФИЛЬТРАЦИЯ: Находим продукты с категорией, содержащей "smartphone"
print("Фильтр по категории 'smartphone':")
filter_category = (
    session.query(Product, Category)
    .select_from(Product)  # Явно указываем основную таблицу
    .join(Product.categories)  # Указываем отношение для JOIN
    .filter(Category.name.like('%smartphone%'))  # Фильтруем по имени категории
    .all()
)
for product, category in filter_category:
    print(f"{product.name} -> {category.name}")