from models import (Base, Product, 
                    session, engine)
import datetime
import csv
import time




if __name__ == '__main__':
    Base.metadata.create_all(engine)
