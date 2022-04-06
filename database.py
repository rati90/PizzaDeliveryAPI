from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite://///home/dev5/PycharmProjects/pizzaAPI/pizza_delivery.db',
                       echo=True
                       )

Base = declarative_base()

Session = sessionmaker()
