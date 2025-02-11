from sqlalchemy import create_engine, Column, VARCHAR, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Создаем базовый класс для моделей
Base = declarative_base()


# Определяем модель Product
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100))
    price = Column(Float)
    quantity = Column(Integer)

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price}, quantity={self.quantity})>"


# Создаем движок
engine = create_engine('sqlite:///products.db')

# Генерируем таблицу на основе модели
Base.metadata.create_all(engine)

# Создаем фабрику сессий
Session = sessionmaker(bind=engine)
session = Session()

# Добавляем новую запись
new_product = Product(name="Phone", price=299.99, quantity=2)
session.add(new_product)
session.commit()

# Выбираем все записи из таблицы
products = session.query(Product).all()
for product in products:
    print(product)

print("Таблица products успешно создана, данные добавлены.")
