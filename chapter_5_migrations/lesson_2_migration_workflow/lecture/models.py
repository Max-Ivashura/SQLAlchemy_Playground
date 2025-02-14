# lecture/models.py
from datetime import datetime

from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)

    def __repr__(self):
        return f"<User(name={self.name}, age={self.age})>"

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer)

    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price})>"

# lecture/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)

    orders = relationship('Order', back_populates='user')

    def __repr__(self):
        return f"<User(name={self.name}, age={self.age})>"

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer)

    orders = relationship('Order', back_populates='product')

    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price})>"

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)  # Новое поле

    user = relationship('User', back_populates='orders')
    product = relationship('Product', back_populates='orders')

    def __repr__(self):
        return f"<Order(user={self.user.name}, product={self.product.name}, quantity={self.quantity}, created_at={self.created_at})>"