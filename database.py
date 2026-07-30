import os
from dotenv import load_dotenv
from peewee import SqliteDatabase

load_dotenv()

BANK_NAME = os.getenv('DB_NAME', 'default.db')

db = SqliteDatabase(BANK_NAME)