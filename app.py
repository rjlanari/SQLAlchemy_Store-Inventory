from sqlalchemy import Integer
from models import (Base, Product, 
                    session, engine)
import datetime
import csv
import time


def menu():
    while True:
        print('''
                \nPRODUCT INVENTORY
                \r
                \rChose a option to continue:
                \r
                \rv-  View the details of a product
                \ra-  Add a new product
                \rb-  Make a backup of the content of the database
                \re-  Exit
                ''')
        choice = input('\rWhat would you like to do? ').lower()
        if choice in ['v', 'a', 'b', 'e']:
            return choice
        else: 
            input('''
                \rPlease enter one of the options in the menu above. 
                \rPress Enter to continue. ''')

def clean_price(price_str): 
    split_price = price_str.split('$')
    price_float = float(split_price[1])
    return int(price_float * 100)


def clean_date(date_str):
    split_date = date_str.split('/')
    month = int(split_date[0])
    day = int(split_date[1])
    year = int(split_date[2])
    return datetime.date(year, month, day)


def clean_id(id_string, option):
    try:
        product_id = int(id_string)
    except ValueError:
        input('''
            \n******** ID ERROR *********
            \rThat ID does not exist.
            \rPress Enter to try again.
            \r **************************
            ''')
        return
    else:
        if product_id in option:
            return product_id
        else:
            return


def view_product(): #handle getting and displaying a product by its product_id
    id_options = []
    for prod in session.query(Product):
        id_options.append(prod.id)
    id_error = True
    while id_error:
        id_chosen = input(f'''
                         \nPlease, enter the ID number between
                         \r{id_options[0]} and {id_options[len(id_options)-1]}
                         \rfor the product you are looking 
                         \rfor:  ''')
        id_chosen = clean_id(id_chosen, id_options)
        if type(id_chosen) == int:
            id_error = False
    chosen_product = session.query(Product).filter(Product.id == id_chosen).first()
    print(f'''\nProduct ID: {chosen_product.id}
              \rName: {chosen_product.product_name} 
              \rStock: {chosen_product.product_quantity} Units
              \rPrice: $ {chosen_product.product_price/100}
              \rLast Updated: {chosen_product.date_updated.strftime("%B %d, %Y")}''')


def add_product():
    name = input("Enter product's name:  ")
    quantity = int(input("Enter the quantity:  "))
    price_error = True
    while price_error:
        price = input('Enter price (ex. $12.44):  ')
        price = clean_price(price)
        if type(price) == int:
            price_error = False
    new_product = Product(product_name=name, product_quantity= quantity, product_price = price, date_updated = datetime.date.today())
    session.add(new_product)
    session.commit()
    print('Product added!')
    time.sleep(2)


def back_up():
    header = ['ID ', 'product_name ', 'product_quantity ', 'product_price ', 'date_updated ']
    with open('back_up_csv', 'w') as cvsfile:
        writer = csv.writer(cvsfile)
        writer.writerow(header)
        prod = session.query(Product)
        for prod in session.query(Product):
            prod_list = []
            prod_list = [prod.id, prod.product_name, prod.product_quantity, prod.product_price, prod.date_updated]
            writer.writerow(prod_list)
        print('Back Up done')
        time.sleep(2)


def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db==None:
                name = row[0]
                price = clean_price(row[1])
                quantity = int(row[2])
                date = clean_date(row[3])
                new_product = Product(product_name=name, product_price=price,product_quantity=quantity, date_updated=date)
                session.add(new_product)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            view_product()
        elif choice == 'a':
            add_product()
        elif choice == 'b':
            back_up()
        else: 
            print('Goodbye!')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()
    #add_csv()
    #clean_price('$2.44')
    #view_product()
    #clean_id('3', [1, 2, 3])
    #add_product()
    #back_up()
    