from peewee import Model, AutoField, TextField
from database import db
from helpers.date_helper import DateHelper

class Account(Model):
    id = AutoField(primary_key=True)
    institution = TextField()
    name = TextField()
    type = TextField()
    card = TextField(null=True)
    created_at = TextField(default=lambda: DateHelper().data_atual_texto())
    updated_at = TextField(default=lambda: DateHelper().data_atual_texto())
    deleted_at = TextField(null=True)

    class Meta:
        database = db
        table_name = 'account'
