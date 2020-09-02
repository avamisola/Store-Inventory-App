from peewee import *


db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = AutoField()
    product_name = CharField()
    product_quantity = IntegerField()
    product_price = DecimalField()
    date_updated = DateField()

    class Meta:
        database = db
        

if __name__ == "__main__":
    db.connect()
    db.create_tables([Product], safe=True)
