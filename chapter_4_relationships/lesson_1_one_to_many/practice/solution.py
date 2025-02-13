from sqlalchemy import Column, Integer, String, Float, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Шаг 1: Создаем базовый класс для моделей
Base = declarative_base()

# Шаг 2: Определяем модели Category и Product
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    products = relationship('Product', back_populates='category')

    def __repr__(self):
        return f'<Category(id={self.id}, name={self.name})>'

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship('Category', back_populates='products')

    def __repr__(self):
        return (f'<Product(id={self.id}, name={self.name}, '
                f'price={self.price}, quantity={self.quantity}, category={self.category.name if self.category else None})>')

# Вспомогательная функция для получения или создания категории
def get_or_create_category(session, name):
    category = session.query(Category).filter_by(name=name).first()
    if not category:
        category = Category(name=name)
        session.add(category)
        session.commit()  # Сохраняем категорию сразу
    return category

# Шаг 3: Создаем движок и связываем его с базовым классом
engine = create_engine('sqlite:///products.db', echo=True)
Base.metadata.create_all(engine)

# Шаг 4: Создаем сессию для работы с данными
Session = sessionmaker(bind=engine)
session = Session()

# Добавляем тестовые данные
phones_category = get_or_create_category(session, 'phones')
laptops_category = get_or_create_category(session, 'laptops')

phone = Product(name='Phone', price=5.99, quantity=1, category=phones_category)
laptop = Product(name='Laptop', price=999.99, quantity=2, category=laptops_category)

session.add_all([phone, laptop])
session.commit()

# Запросы с использованием отношений
print("Продукты и их категории:")
for product in session.query(Product).all():
    print(f"{product.name}:")
    if product.category:
        print(f"  - {product.category.name}")
    else:
        print("  - Категория не указана")

# Обратная ссылка: Находим продукты по категории
category_name = 'phones'
category = session.query(Category).filter_by(name=category_name).first()
if category:
    print(f"Категория {category.name} содержит следующие продукты:")
    for product in category.products:
        print(f"  - {product.name}")
else:
    print(f"Категория '{category_name}' не найдена.")