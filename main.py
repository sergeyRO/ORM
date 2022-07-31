import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from model import create_tables, Book, Publisher, Stock, Sale, Shop
from dotenv import dotenv_values

for item in dotenv_values().items():
    if item[0] == 'DSN':
        DSN = item[1]
        break

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as f:
    data = json.load(f)
for item in data:
    model = {
        'publisher': Publisher,
        'book': Book,
        'shop': Shop,
        'stock': Stock,
        'sale': Sale
    }.get(item['model'])
    session.add(model(id=item.get('pk'), **item.get('fields')))
session.commit()

publisher_id = input('Введите ID издателя: ')
print(session.query(Publisher).filter(Publisher.id == publisher_id).first())

# добавьте запрос выборки магазинов, где продаются книги целевого издателя
shop_publisher = session.query(Shop, Shop.id, Shop.name)\
    .join(Stock, Shop.id == Stock.id_shop)\
    .join(Book,Stock.id_book == Book.id)\
    .filter(Book.id_publisher == publisher_id, ).all()
if len(shop_publisher) != 0:
    print(f'Магазины в которых продаются книги издателя с ID={publisher_id}')
    for item in shop_publisher:
        print(f'ID: {item[1]} ===> Наименование: {item[2]}')
else:
    print('Нет ни одного магазина')

session.close()
