# lecture/test.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Product, Order

# Создаем движок
engine = create_engine('sqlite:///database.db', echo=True)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Добавляем тестовые данные
alice = User(name="Alice", age=30)
phone = Product(name="Phone", price=199)
order = Order(user=alice, product=phone, quantity=2)

session.add_all([alice, phone, order])
session.commit()

# Проверяем данные
print("Пользователи:")
for user in session.query(User).all():
    print(user)

print("Продукты:")
for product in session.query(Product).all():
    print(product)

print("Заказы:")
for order in session.query(Order).all():
    print(order)