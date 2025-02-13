from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'  # Используйте множественное число для имени таблицы

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'))

    # Связь с самой собой
    parent = relationship('Category', remote_side=[id], back_populates='subcategories')
    subcategories = relationship('Category', back_populates='parent')

    def __repr__(self):
        return f'<Category(id={self.id}, name="{self.name}")>'

# Шаг 3: Создаем движок и связываем его с базовым классом
engine = create_engine('sqlite:///categories.db', echo=True)
Base.metadata.create_all(engine)

# Шаг 4: Создаем сессию для работы с данными
Session = sessionmaker(bind=engine)
session = Session()

# Добавляем тестовые данные
category_0 = Category(name='Electronic')
category_1 = Category(name='PC', parent=category_0)
category_2 = Category(name='Laptop', parent=category_0)
category_3 = Category(name='Phone', parent=category_0)

session.add_all([category_0, category_1, category_2, category_3])
session.commit()

# Запросы с использованием селф-референциального отношения
print("Субкатегории и их категории:")
for category in session.query(Category).all():  # Используйте category вместо employee
    print(f"{category.name}:")
    if category.parent:
        print(f"  - Родительская категория: {category.parent.name}")
    else:
        print("  - Родительская категория отсутствует.")

print("\nКатегории и их субкатегории:")
for category in session.query(Category).all():
    if category.subcategories:
        print(f"{category.name} содержит следующие подкатегории:")
        for subcategory in category.subcategories:
            print(f"  - {subcategory.name}")
    else:
        print(f"{category.name} не содержит подкатегорий.")