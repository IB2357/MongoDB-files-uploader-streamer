from  connect import * 



# Define the change stream pipeline to exclude documents with {'watcher': 'watched'}
pipeline = [
    {"$match": {
            "fullDocument.watcher": {"$ne": "watched"},
            "operationType": {"$ne": "delete"}
        }
    }
]

# Watch the collection for changes with the specified filter
change_stream = collection.watch(pipeline=pipeline, full_document='updateLookup')
print("Watching for changes...")


collection.update_many({"watcher":{"$exists":False}},{"$set":{"watcher":"ready"}})


try:
    for change in change_stream:

        print('='*60,'\n',change,'\n','='*60)
        print(type(change))

        
        collection.update_one(
            {'_id': change['documentKey']['_id']},
            {'$set': {'watcher': 'watched'}}
        )
except KeyboardInterrupt:
    print("\n\n\t\tfiles watcher has been stopped.")


