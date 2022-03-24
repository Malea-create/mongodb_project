import pymongo
from pymongo import MongoClient
import pprint

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

customers_info = mydb["customers_info"] 
customers_hobbies = mydb["customers_hobbies"] 

info = [
  { "name": "William", "address": "Central st 954"},
  { "name": "Chuck", "address": "Main Road 989"},
  { "name": "Viola", "address": "Sideway 1633"}
]

mydb.customers_info.insert_many(info)

hobbies = [
  { "name": "William", "hobby": "Basketball"},
  { "name": "Chuck", "hobby": "Soccer"},
  { "name": "Viola", "hobby": "Ballet"}
]

mydb.customers_hobbies.insert_many(hobbies)

pprint.pprint ( mydb.list_collection_names() ) 

pipeline_agg = [ # pipline = array of multiple elements

            {"$lookup":
                {
                "from": "customers_hobbies",
                "localField": "name",
                "foreignField": "name",
                "as": "hobby_info"
                }
            },
            { "$project": 
                {
                  "_id": "$_id", 
                  "address": "$address", 
                  "hobby": "$hobby_info.hobby", 
                  "name": "$name", 
                }
            },
            { # out processing stage 
                    "$out":"customers_info"
                }
        ]


mydb.customers_info.aggregate(pipeline_agg)


cursor = mydb.customers_info.find()

for doc in cursor:
    pprint.pprint (doc)


#drop
mydb.customers_hobbies.drop()
mydb.customers_info.drop()
pprint.pprint ( mydb.list_collection_names() ) 

