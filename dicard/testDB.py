# Installing PyMongo by using $ pip install pymongo==3.11.2
import pymongo # to low level ??????
import pprint

# estabilshing a connection
from pymongo import MongoClient
client = MongoClient() # create MongoClient instance (provides a client for a MongoDB instance or server)

client # connection to the default host (localhost) and port (27017)
#client = MongoClient(host="localhost", port=27017) # provide a custom host and port
#client = MongoClient("mongodb://localhost:27017") # MongoDB URI format

db = client.rptutorials # access any database managed by the specified MongoDB server
db

# pprint library is used to make the output look more pretty
#from pprint import pprint
# Issue the serverStatus command and print the results
#serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)

# create document

tutorial1 = {
    "title": "Working With JSON Data in Python",
    "author": "Lucas",
    "contributors": [
        "Aldren",
        "Dan",
        "Joanna"
        ],
        "url": "https://realpython.com/python-json/"
        }

tutorial = db.tutorial # specify which collection to use
tutorial

# insert documents into tutorial by calling .insert_one() on it with a document as an argument

result = tutorial.insert_one(tutorial1) # .insert_one() takes tutorial1, inserts it into the tutorial collection and returns an InsertOneResult object
result
print(f"One tutorial: {result.inserted_id}")

# .insert_many() to insert many tutorials into one document 

tutorial2 = {
    "title": "Python's Requests Library (Guide)",
    "author": "Alex",
    "contributors": [
        "Aldren",
        "Brad",
        "Joanna"
        ],
        "url": "https://realpython.com/python-requests/"
        }

tutorial3 = {
    "title": "Object-Oriented Programming (OOP) in Python 3",
    "author": "David",
    "contributors": [
        "Aldren",
        "Joanna",
        "Jacob"
        ],
        "url": "https://realpython.com/python3-object-oriented-programming/"
        }

new_result = tutorial.insert_many([tutorial2, tutorial3])

print(f"Multiple tutorials: {new_result.inserted_ids}")

# retrieve documents from a collection

import pprint

for doc in tutorial.find(): # use .find(). Without arguments, .find() returns a Cursor object that yields the documents in the collection on demand
    pprint.pprint(doc) # pprint.pprint() to provide a user-friendly output format

#.find_one() to retrieve a single document
jon_tutorial = tutorial.find_one({"author": "Lucas"})
pprint.pprint(jon_tutorial)

client.close() # keep your connection alive and only close it before exiting the application to clear all the acquired resources / connection to a MongoDB database is typically an expensive operation

pprint.pprint(client.list_database_names()) #see availible db