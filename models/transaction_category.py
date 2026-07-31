from database import db
from helpers.date_helper import DateHelper
from peewee import Model, AutoField, TextField


class TransactionCategory(Model):
    id = AutoField(primary_key=True)
    name = TextField()
    departament = TextField()
    created_at = TextField(default=lambda: DateHelper().data_atual_texto())
    updated_at = TextField(default=lambda: DateHelper().data_atual_texto())
    deleted_at = TextField(null=True)

    class Meta:
        database = db
        table_name = 'transaction_category'
