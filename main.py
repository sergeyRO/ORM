import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from model import create_tables, Book, Publisher, Stock, Sale, Shop

DSN = "postgresql://postgres:password@localhost:5432/ORM_DB"
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

print(session.query(Publisher).filter(Publisher.id == input('Введите ID издателя: ')).first())

session.close()
