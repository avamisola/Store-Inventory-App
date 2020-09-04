import csv

from datetime import date
from datetime import datetime

from peewee import *


db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = AutoField()
    product_name = CharField(max_length=255, unique=True)
    product_quantity = IntegerField(default=0)
    product_price = IntegerField(default=0)
    date_updated = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        

if __name__ == "__main__":

    db.connect()
    db.create_tables([Product], safe=True)

#    with open('requirements.txt', 'a') as csvfile:
#        fieldnames = ['product_name','product_price','product_quantity','date_updated']
#        productwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)


    def read_csv():
        """read csv data into dictionary and clean data"""
        with open('inventory.csv', newline='') as csvfile:
            product_reader = csv.DictReader(csvfile, delimiter=',')
            rows = list(product_reader)
            product_list = []
            for row in rows:
                converted_price = float(row['product_price'].replace('$','')) * 100
                row['product_price'] = round(converted_price)
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

    add_products()