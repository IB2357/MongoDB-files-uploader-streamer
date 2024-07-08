from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import bson
from datetime import datetime

import os
from os import getenv
import time
import shutil

from dotenv import load_dotenv
load_dotenv() # to get env vars from .env


# CONFIGS
client = MongoClient(getenv('CONNECT_STR'))
db = client[getenv('DATABASE')]
collection = db[getenv('COLLECTION')]
folder_path = 'source'  
processed_folder_path = 'archive'  
allowed_extensions = {'.pdf', '.xml', '.txt'}  
watcher_delay = 1 # in second
batch_size = 1 # int



try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("MongoDB server is available")
except ConnectionFailure:
    print("Server not available")


def _is_valid_file(file_path, filename):
    return (
        os.path.isfile(file_path)
        and os.path.splitext(filename)[1] in allowed_extensions
    )

def _move_to_processed(file_path, filename):
    processed_file_path = os.path.join(processed_folder_path, filename)
    shutil.move(file_path, processed_file_path)  


os.makedirs(processed_folder_path, exist_ok=True) # create if not exist 

try:
    while True:
        # print('watching ...')
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            file_extention = os.path.splitext(filename)[1]
            print(os.path.splitext(filename), '\n\n\n\n')

            if _is_valid_file(file_path, filename):
                if file_extention in ['.pdf']:
                    with open(file_path, 'rb') as file:
                        file_contents = file.read()
                        doc = {
                            "file_name": os.path.splitext(filename)[0],
                            "file_extention": os.path.splitext(filename)[1],
                            "upload_date": datetime.now(),
                            "file_contents": bson.Binary(file_contents)
                        }
                else:
                    with open(file_path, 'r') as file:
                        file_contents = file.read()
                        doc = {
                            "file_name": os.path.splitext(filename)[0],
                            "file_extention": os.path.splitext(filename)[1],
                            "upload_date": datetime.now(),
                            "file_contents": file_contents
                        }

                _move_to_processed(file_path,filename)
        
                collection.insert_one(doc)


        # print(f'sleep for {watcher_delay} sec ...')
        time.sleep(watcher_delay)  # Wait before checking for new files

except KeyboardInterrupt:
    print("\n\n\t\tfiles uploader has been stopped.")


