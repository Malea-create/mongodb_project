import pymongo
from pymongo import MongoClient
import pandas as pd
import json

### Create Database, Collections and callable Algorightm ###

'''
this file stores all functions to properly create collections and check the result

therefore it includes:
- add_collection_to_db() reads csv into pandas df, converts df in json in order to insert the data into a new collection
- show_collections() lists all collections for a database
'''

# Loding Data into Mongo DB (adding Collections to DB)

def add_collection_to_db(filepath, db, collection_name):

    # Create collection (*aka* table)
    db_collection = db[collection_name] 

    # Add data to collection 
    data = pd.read_csv(filepath, sep=";")
    data_json = json.loads(data.to_json(orient='records')) # parse csv to json 
    db_collection.insert_many(data_json, ordered=False) # insert json in collection

def show_collections(db, db_name):
    print('The following collections have been added to', db_name, ':')
    for coll in db.list_collection_names(): #see available collections in db DB
        print('- ', coll)



