import pymongo
from pymongo import MongoClient
import functions
import pprint

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

mylist = [
  { "name": "William", "address": "Central st 954"},
  { "name": "Chuck", "address": "Main Road 989"},
  { "name": "Viola", "address": "Sideway 1633"}
]

#mydb.customers.insert_many(mylist)

pprint.pprint ( mydb.list_collection_names() ) 

cursor = mydb.customers.find()
for doc in cursor:
    pprint.pprint (doc)

pipeline = [ # pipline = array of multiple elements

            { # match processing stage 
                "$match": # equal to find
                { "name": { "$ne": "Viola" } } # value/ querie
            },
            { 
                "$merge": 
                {"into": "newcoll",
                "on": "_id",
                "whenMatched": "keepExisting", 
                "whenNotMatched": "insert"  }
            }
        ]

mydb.customers.aggregate(pipeline)

cursor = mydb.newcoll.find()
for doc in cursor:
    pprint.pprint( "Inside the newcoll:" )
    pprint.pprint (doc)

'''
#drop
mydb.customers.drop()
mydb.newcoll.drop()
mydb.mycol.drop()
pprint.pprint ( mydb.list_collection_names() ) 
'''