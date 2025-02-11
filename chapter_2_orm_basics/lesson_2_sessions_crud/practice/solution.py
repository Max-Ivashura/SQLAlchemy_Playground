from sqlalchemy import Column, VARCHAR, Float, Integer, create_engine
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
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, quantity={self.quantity})>"

# Создаем движок
engine = create_engine('sqlite:///products.db')

# Генерируем таблицу на основе модели
Base.metadata.create_all(engine)

# Создаем фабрику сессий
Session = sessionmaker(bind=engine)
session = Session()

# CREATE: Добавляем новую запись
new_product = Product(name="Phone", price=299.99, quantity=2)
session.add(new_product)
session.commit()
print("Запись успешно добавлена.")

# READ: Выбираем все записи
products = session.query(Product).all()
for product in products:
    print(product)

# UPDATE: Обновляем цену продукта
product_to_update = session.query(Product).filter_by(name="Phone").first()
if product_to_update:
    product_to_update.price = 246.75
    session.commit()
    print("Запись успешно обновлена.")
else:
    print("Ошибка: Запись для обновления не найдена!")

# DELETE: Удаляем продукт
product_to_delete = session.query(Product).filter_by(name="Phone").first()
if product_to_delete:
    session.delete(product_to_delete)
    session.commit()
    print("Запись успешно удалена.")
else:
    print("Ошибка: Запись для удаления не найдена!")