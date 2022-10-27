from sqlalchemy import(create_engine, Column, 
                        Integer, String, Date)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    product_name = Column('Name', String)
    product_price = Column('Price', Integer)
    product_quantity = Column('Quantity', Integer)
    date_updated = Column('Updated', Date   )

    def __repr__(self):
        return f'ID: {self.id}, {self.product_name}, Quantity {self.product_quantity}, Price {self.product_price}, Updated nn {self.date_updated} '




