import pymongo
from pymongo import MongoClient
import setup_functions
import pprint
import pipelines

'''
1) Create Connection/Db/Collections
2) Create Piplines (Input: Titel -> Retrieve ISBN, Users how read Isbn, all other ISBNs read by user)
3) Link Pilines together

take care: input can not be included in result
Next step:
- add error handeling
- remove inspection lines
'''

# Establish connection with Mongo DB and create DB
client = MongoClient('mongodb://localhost:27017') # connect now to save db, ...
#pprint.pprint(client.list_database_names()) #see availible db

# Create DB in Mongo DB
db_name = 'BookCrossing_DB'
db = client[db_name] # Creating a database

def collection_setup():

    # Create collections for each csv file 

    setup_functions.add_collection_to_db('data/BX-Book-Ratings.csv', db, 'book_ratings') # pass csv file path and collection name 
    setup_functions.add_collection_to_db('data/BX-Books.csv', db, 'books') # pass csv file path and collection name 
    setup_functions.add_collection_to_db('data/BX-Users.csv', db, 'user') # pass csv file path and collection name 
    setup_functions.show_collections(db, db_name)


def get_recommendations(user_input):

    db.recommendations.drop() # needs to be emptied every time (storage for new results)
    pipelines.get_isbn(user_input) # start Process

    # pass isbn results to next pipline

    isbn_results = db.isbns.find()

    for doc in isbn_results:
            pipelines.get_userids(doc["_id"])
            isbn = doc

    # pass user results to next pipline

    userid_results = db.readers.find().limit(50) # else too time consuming

    for doc in userid_results:
            pipelines.get_books_w_merge(doc["_id"])

    # reshape recommendations

    pipelines.reshape_recommendations(isbn)

    # inspect results
'''
get_recommendations("Tell Me This Isn't Happening")

recommendation_results = db.recommendations_reshaped.find().limit(5) # get frist 10 records (high rated)

for doc in recommendation_results: # get result and additional info
    rating = str ( doc["Rating"] )
    count = str ( doc["Count"] )
    isbn = doc["_id"]
    pprint.pprint( db.books.find_one({"ISBN":doc["_id"]})["Book_Title"]) 
    pprint.pprint( "Rating: " + rating + " / ISBN: " + isbn + " / Count: " + count)
'''