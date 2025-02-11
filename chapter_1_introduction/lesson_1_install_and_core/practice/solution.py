from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select, Float

engine = create_engine('sqlite:///solution.db')
metadata = MetaData()

products_table = Table(
    'products', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(100), unique=True, nullable=False),
    Column('price', Float),
    Column('quantity', Integer),
)

metadata.create_all(engine)
print("Таблица products успешно создана.")

with engine.connect() as connection:
    insert_stmt = products_table.insert().values(name="Laptop", price=10.99, quantity=2)
    connection.execute(insert_stmt)
    connection.commit()

print("Запись успешно добавлена.")

with engine.connect() as connection:
    # Выбираем все записи из таблицы products
    query = select(products_table)
    result = connection.execute(query)
    for row in result:
        print(row)
