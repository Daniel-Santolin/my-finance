from database import db
from peewee import Model, AutoField, IntegerField, TextField, ForeignKeyField
from account import Account
from transaction_category import TransactionCategory

class Transaction(Model):
    id = AutoField(primary_key=True)
    account = ForeignKeyField(Account, column_name='account_id', backref='transactions')
    transaction_category = ForeignKeyField(
        TransactionCategory, 
        column_name='transaction_category_id', 
        null=True, 
        backref='transactions'
    )
    type = TextField()
    date = TextField()
    name = TextField()
    alias = TextField(null=True)
    value = IntegerField(default=0)
    status = TextField()
    created_at = TextField()
    updated_at = TextField()
    deleted_at = TextField(null=True)

    class Meta:
        database = db
        table_name = 'transaction'