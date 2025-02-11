from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, VARCHAR, DateTime, Float

engine = create_engine('sqlite:///solution.db')
metadata = MetaData()

orders_table = Table('orders', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('customer_name', VARCHAR(100)),
                     Column('order_date', DateTime),
                     Column('total_amount', Float), )

metadata.create_all(engine)
print('База данных создана!')

# Add row in table
with engine.connect() as connection:
    insert_stmt = orders_table.insert().values(customer_name='BigCustomer',
                                               order_date=datetime.now(), total_amount=5.0)
    connection.execute(insert_stmt)
    connection.commit()

# Print All rows
with engine.connect() as connection:
    result = connection.execute(orders_table.select())
    for row in result:
        print(row)

# Update row
with engine.connect() as connection:
    update_stmt = orders_table.update().where(orders_table.c.customer_name == 'BigCustomer').values(total_amount=15.0)
    connection.execute(update_stmt)
    connection.commit()

# Delete row
with engine.connect() as connection:
    delete_stmt = orders_table.delete().where(orders_table.c.customer_name == 'BigCustomer')
    connection.execute(delete_stmt)
    connection.commit()

print("CRUD-операции успешно выполнены.")
