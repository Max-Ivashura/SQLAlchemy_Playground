# test.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Product

# Создаем движок
engine = create_engine('sqlite:///database.db', echo=True)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Добавляем тестовые данные
new_user = User(name="Alice", age=30)
new_product = Product(name="Phone", price=199)

session.add_all([new_user, new_product])
session.commit()

# Проверяем данные
print("Пользователи:")
for user in session.query(User).all():
    print(user)

print("Продукты:")
for product in session.query(Product).all():
    print(product)