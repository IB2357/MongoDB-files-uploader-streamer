from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import bson
from datetime import datetime
from os import getenv
from dotenv import load_dotenv
load_dotenv() # to get env vars from .env


# CONFIGS
client = MongoClient(getenv('CONNECT_STR'))
db = client[getenv('DATABASE')]
collection = db[getenv('COLLECTION')]


try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("MongoDB server is available")
except ConnectionFailure:
    print("Server not available")