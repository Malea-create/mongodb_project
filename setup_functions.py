import pymongo
from pymongo import MongoClient
import pandas as pd
import json


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



