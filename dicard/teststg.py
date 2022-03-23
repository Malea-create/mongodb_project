import pymongo
from pymongo import MongoClient
import pprint

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

info = [
  { "name": "William", "address": "Central st 954"},
  { "name": "Chuck", "address": "Main Road 989"},
  { "name": "Viola", "address": "Sideway 1633"}
]

hobbies = [
  { "name": "William", "hobby": "Basketball"},
  { "name": "Chuck", "hobby": "Soccer"},
  { "name": "Viola", "hobby": "Ballet"}
]

mydb.customers_info.insert_many(info)
mydb.customers_hobbies.insert_many(hobbies)

pprint.pprint ( mydb.list_collection_names() ) 

pipeline = [ # pipline = array of multiple elements

            {"$lookup":
                {
                "from": "customers_hobbies",
                "localField": "name",
                "foreignField": "name",
                "as": "hobbies"
                }
            }
        ]

mydb.customers_info.aggregate(pipeline)

cursor = mydb.customers_info.find()

for doc in cursor:
    pprint.pprint (doc)

'''
#drop
mydb.customers.drop()
mydb.newcoll.drop()
mydb.mycol.drop()
pprint.pprint ( mydb.list_collection_names() ) 
'''