from database import db
from helpers.date_helper import DateHelper
from models.account import Account
from models.transaction_category import TransactionCategory
from peewee import Model, AutoField, IntegerField, TextField, ForeignKeyField


class Transaction(Model):
    id = AutoField(primary_key=True)
    account = ForeignKeyField(Account, column_name='account_id', backref='transactions')
    transaction_category = ForeignKeyField(
        TransactionCategory, 
        column_name='transaction_category_id', 
        null=True, 
        backref='transactions'
    )
    transaction_type = TextField()
    date = TextField()
    name = TextField()
    alias = TextField(null=True)
    value = IntegerField(default=0)
    status = TextField()
    created_at = TextField(default=lambda: DateHelper().data_atual_texto())
    updated_at = TextField(default=lambda: DateHelper().data_atual_texto())
    deleted_at = TextField(null=True)

    class Meta:
        database = db
        table_name = 'transaction'