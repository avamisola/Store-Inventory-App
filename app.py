import csv
import sys

from datetime import date
from datetime import datetime

from peewee import *
from playhouse.shortcuts import model_to_dict


db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = AutoField()
    product_name = CharField(max_length=255, unique=True)
    product_quantity = IntegerField(default=0)
    product_price = IntegerField(default=0)
    date_updated = DateTimeField(default=datetime.now)

    class Meta:
        database = db


def initialize():
    """connect db, create db and table if don't exist"""
    db.connect()
    db.create_tables([Product], safe=True)


def convert_price(price):
    """convert dollar price to cents"""
    return int(round(float(price.replace('$','')) * 100))


def read_csv():
    """read csv data into dictionary and clean data"""
    with open('inventory.csv', newline='') as csvfile:
        product_reader = csv.DictReader(csvfile, delimiter=',')
        rows = list(product_reader)
        product_list = []
        for row in rows:
            row['product_price'] = convert_price(row['product_price'])
            converted_date = datetime.strptime(row['date_updated'], '%m/%d/%Y')
            row['date_updated'] = datetime.combine(converted_date, datetime.min.time())
            product_list.append(row)
        return product_list


def add_products():
    """add cleaned data from csv to database"""
    products = read_csv()
    for product in products:
        try:
            Product.create(product_name=product['product_name'],
                            product_price=product['product_price'],
                            product_quantity=product['product_quantity'],
                            date_updated=product['date_updated'])
        except IntegrityError:
            product_record = Product.get(product_name=product['product_name'])
            product_record.product_price = product['product_price']
            product_record.product_quantity = product['product_quantity']
            product_record.date_updated = product['date_updated']
            product_record.save()


def menu_loop():
    """show the menu"""
    choice_main = None

    print("""\n
======================================================
--Welcome to the Store Inventory Database--\n
Select an option by entering the corresponding letter\n
v) View entry in database
a) Add entry to database
b) Backup the database to csv
q) Quit the app
======================================================
    """)

    choice_main = input("Enter letter to select option: ").lower().strip()

    if choice_main == 'v':
        view_entry()
    elif choice_main == 'a':
        add_entry()
    elif choice_main == 'b':
        backup_database()
    elif choice_main == 'q':
        quit_app()
    else:
        error_handler()
        

def view_entry():
    """view entry in database by product id"""
    choice_view = None
    choice_view = input("Enter product_id to view entry: ").lower().strip()

    if choice_view == 'v':
        view_entry()
    else:
        error_handler()


def add_entry():
    """add entry to database"""
    try:
        name_input = input("Enter product name: ")
        qty_input = int(input("Enter product quantity: "))
        price_input = convert_price(input("Enter product price: "))
    except ValueError:
        error_handler()
    



def backup_database():
    """backup the database to csv"""
    db_data = [model_to_dict(item) for item in Product.select().order_by(Product.product_id)]

    with open('backup.csv', 'w', newline='') as csvfile:
        fieldnames = ['product_id',
                    'product_name',
                    'product_price',
                    'product_quantity',
                    'date_updated']
        productwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        productwriter.writeheader()
        productwriter.writerows(db_data)

    print("\n\nDatabase table has been backed up to backup.csv")
    continue_prompt()


def quit_app():
    """quit the application"""
    print("\n\nThank you for using this app. Goodbye!")
    print("\n\n----END----\n\n")
    sys.exit()


def error_handler():
    """generic error message and reroute to main menu choice"""
    print("\n\nThat is not a valid option, please choose again.")
    continue_prompt()


def continue_prompt():
    """prompt to press enter to continue back to main menu"""
    input("\nPress ENTER to continue...")
    menu_loop()


if __name__ == "__main__":
    initialize()
    add_products()
    menu_loop()
