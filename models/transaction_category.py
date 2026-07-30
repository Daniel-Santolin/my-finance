from peewee import Model, AutoField, TextField
from database import db

class TransactionCategory(Model):
    id = AutoField(primary_key=True)
    name = TextField()
    departament = TextField()
    created_at = TextField()
    updated_at = TextField(null=True)
    deleted_at = TextField(null=True)

    class Meta:
        database = db
        table_name = 'transaction_category'
