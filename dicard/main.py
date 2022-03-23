import pymongo
from pymongo import MongoClient
import functions
import pprint


# Establish connection with Mongo DB and create DB
client = MongoClient('mongodb://localhost:27017') # connect now to save db, ...
#pprint.pprint(client.list_database_names()) #see availible db

# Create DB in Mongo DB
db_name = 'BookCrossing_DB'
db = client[db_name] # Creating a database

'''
# Create collections for each csv file 
functions.add_collection_to_db('data/BX-Book-Ratings.csv', db, 'book_ratings') # pass csv file path and collection name 
functions.add_collection_to_db('data/BX-Books.csv', db, 'books') # pass csv file path and collection name 
functions.add_collection_to_db('data/BX-Users.csv', db, 'user') # pass csv file path and collection name 
functions.show_collections(db, db_name)
'''
read = "Classical Mythology"

pipline = [ # pipline = array of multiple elements

        { #processing stage 
            "$match": # equal to find
            { "Book-Title":read } #value/ querie
        }
    ]

pprint.pprint (db.books.aggregate(pipline))

'''
#Add all readers to book and calculate rating 
pipeline = [{'$lookup': 
                {'from' : 'book_ratings',
                 'localField' : 'ISBN',
                 'foreignField' : 'ISBN',
                 'as' : 'User-ID'}},
            {'$unwind': '$User-ID'}
             ]

db.books.aggregate(pipeline)
pprint.pprint (db.books.find_one())
'''
'''
aggregate_pipline =[
      {"$lookup":{
        from: "book_ratings",       # other table name
        localField: "ISBN",   # name of users table field
        foreignField: "ISBN", # name of userinfo table field
        as: "User-ID"         # alias for userinfo table
      },
       {   "$unwind":"$user_info" },     # $unwind used for getting data in object or for one record only
      ]
db.book.aggregate(aggregate_pipline)
'''
'''
# Clean and Reorganize


querie = db.user.find_one() #.find_one() to retrieve a single document aka one record
pprint.pprint(querie) # pprint.pprint() to provide a user-friendly output format

# prepare aggregate pipeline with $project and $match
aggregate_pipline =[
      {
        "$project": {
          "Location": {
                "$split": [
                  "$Location",
                  ","
                ] },
          "User-ID": "$User-ID",
          "Age": "$Age"
        }
      }
    ]

# aggregate query

db.user.update_many({}, aggregate_pipline)


querie2 = db.user.find_one() #.find_one() to retrieve a single document aka one record
pprint.pprint(querie2) # pprint.pprint() to provide a user-friendly output format
'''

'''
{'Age': None,
 'Location': 'nyc, new york, usa',
 'User-ID': 1,
 '_id': ObjectId('62367cdd744aebb8014f64c4')}

 ->

{'Age': None,
 'Location': ['nyc', ' new york', ' usa'],
 'User-ID': 1,
 '_id': ObjectId('62367cdd744aebb8014f64c4')}
'''


# delecet ratings < 5 
#db.book_ratings.deleteMany({"BookRating":0})

# curor is a tool to iterate over queries

# get ISBN from search 
#read = "Classical Mythology"
#ob_id = db.books.find_one({"Book-Title":read})["_id"]
#isbn = db.books.find_one({"Book-Title":read})["ISBN"] #filter,projection (projections, you can return specific key/value pairs)
#pprint.pprint(db.books.find_one({"ISBN":isbn})) # check result
#pprint.pprint ( ob_id )


#user_ids = list ( db.book_ratings.find({"ISBN":isbn}))

#db.books.update({}, {"$set": {"read_by": ""}},False,True) # add new empty column
#db.books.update_one({ "_id" : ob_id }, {"$set": {"read_by": user_ids }},False,True) # add array to field for faster retrieval 
#pprint.pprint(db.books.find_one({ "_id" : ob_id }))

#users = db.books.find_one({ "_id" : ob_id },{"read_by" :1})#["read_by"]
#pprint.pprint( users )

#books = list ( db.book_ratings.find({ "User-ID" : "276747" }) )#["read_by"]
#pprint.pprint(books)

#db.books.update({}, {'$unset': {"read_by": ""}}, False, True)
#pprint.pprint(db.books.find_one())

'''
# list user IDs according to ISBN
result = list ( db.book_ratings.find({"ISBN":isbn},{"UserID":1,"_id":0}))
for doc in result:
     print(doc)
'''



# Querie schneller machen nested data (group by User / usbn)
# add read by users as list to books da and group users 

'''
The find method returns a Cursor instance, which allows you to iterate over all matching documents.

To get the first document that matches the given criteria you need to use find_one. The result of find_one is a dictionary.

You can always use the list constructor to return a list of all the documents in the collection but bear in mind that this will load all the data in memory and may not be what you want.'''