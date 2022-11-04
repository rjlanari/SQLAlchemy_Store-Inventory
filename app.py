from tkinter.messagebox import NO
from sqlalchemy import Integer, true
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
    return datetime.datetime(year, month, day)


def clean_id(id_string, option):
    try:
        product_id = int(id_string)
    except ValueError:
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
        else: 
            print('''\n****** ID ERROR *******
                     \rThat ID does not exist.
                     \rPlease, try again.
                     \r***********************''')
    chosen_product = session.query(Product).filter(Product.id == id_chosen).first()
    print(f'''\nProduct ID: {chosen_product.id}
              \rName: {chosen_product.product_name} 
              \rStock: {chosen_product.product_quantity} Units
              \rPrice: $ {chosen_product.product_price/100}
              \rLast Updated: {chosen_product.date_updated.strftime("%B %d, %Y")}''')


def add_product():
    name = input("Enter product's name:  ")     
    try:    
        quantity = int(input("Enter the quantity:  "))
    except ValueError:
        input('''\n****** Quantity Error ******
                 \rPlease enter a valid number.
                 \rPress Enter to continue.
                 \r**************************''')
        return
    price_error = True
    while price_error:
        price = input('Enter price (ex. $12.44):  ')
        try:
            price = clean_price(price)
            price_error = False
        except IndexError: 
            input('''\n***** Price Error *****
                    \rDon't forget the $ sign.
                    \rPress Enter to continue.
                    \r************************''')
        except ValueError:
            input('''\n***** Price Error *****
                    \rPlease, enter a number 
                    \rwith dot instead of coma.
                    \rPress Enter to continue.
                    \r************************''')
    previous_entry = session.query(Product).filter(Product.product_name == name).one_or_none()
    if previous_entry == None:
        new_product = Product(product_name=name, product_quantity= quantity, product_price = price, date_updated = datetime.datetime.today())
        session.add(new_product)
        print('Product Added!')
    else: 
        previous_entry.product_quantity = quantity
        previous_entry.product_price = price
        previous_entry.date_updated = datetime.date.today()
        print('Product Updated!')
    session.commit()
    time.sleep(2)


def back_up():
    header = ['product_name','product_price','product_quantity','date_updated']
    with open('backup.csv', 'w') as cvsfile:
        writer = csv.writer(cvsfile)
        writer.writerow(header)
        for prod in session.query(Product):
            prod_list = []
            price = '$'+ format(prod.product_price/100, '.2f')
            split_date = str(prod.date_updated).split('-')
            month = split_date[1]
            day = split_date[2].split(' ')[0]
            #timetime = split_date[2].split(' ')[1]
            year = split_date[0]
            date = f'{month}/{day}/{year}'
            prod_list = [prod.product_name, price, prod.product_quantity, date]
            writer.writerow(prod_list)
        print('Back Up done')
        time.sleep(2)


def add_csv(): 
    with open('inventory.csv') as csvfile:
        next(csvfile)  
        data = csv.reader(csvfile)
        names = []
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db==None:
                name = row[0]
                names.append(name)
                price = clean_price(row[1])
                quantity = int(row[2])
                date = clean_date(row[3])
                new_product = Product(product_name=name, product_price=price,product_quantity=quantity, date_updated=date)
                session.add(new_product)
            else:
                product_in_db.product_quantity = int(row[2])
                product_in_db.product_price = clean_price(row[1])
                product_in_db.date_updated = clean_date(row[3])
        print('Product Updated!')
                        
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
    
    add_csv()
    app()
    #view_product()
    #add_product()
    #back_up()
    #session.delete(prod)
    
    for p in session.query(Product):
          print(p)