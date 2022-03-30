import pymongo
from pymongo import MongoClient
import setup_functions
import pprint
import pipelines
import pandas as pd


### Create Database, Collections and callable Algorightm ###

'''
the main purpose of this file is to call all funktions from other files in order to get one function,
that includes the program logic/ alogrightm

therefore it includes:
- collection_setup() create collections and uses the setup_functions to create collections
- get_recommendations() link the pielines together and hands down the results from the previous aggregations,
  save result in new collection called recommendations_reshaped
'''

# Establish connection with Mongo DB and create DB
client = MongoClient('mongodb+srv://Malea:12345678@cluster0.nbcni.mongodb.net/myFirstDatabase?retryWrites=true&w=majority') # connect now to save db, ...
#pprint.pprint(client.list_database_names()) #see availible db

# Create DB in Mongo DB
db_name = 'BookCrossing_DB'
db = client[db_name] # Creating a database

def collection_setup(): 

    # Create collections for each csv file 

    setup_functions.add_collection_to_db('data/BX-Book-Ratings.csv', db, 'book_ratings') # pass csv file path and collection name 
    setup_functions.add_collection_to_db('data/BX-Books.csv', db, 'books') # pass csv file path and collection name 
    setup_functions.add_collection_to_db('data/BX-Users.csv', db, 'user') # pass csv file path and collection name 
    setup_functions.show_collections(db, db_name) # inspect results


def get_recommendations(user_input):

    db.recommendations.drop() # needs to be emptied every time (storage for new results)

    pipelines.get_isbn(user_input) # search for matching isbn to user_input /start Process

    # pass isbn results to next pipline

    isbn_results = db.isbns.find_one()
    
    pipelines.get_userids(isbn_results["_id"])


    # pass user results to next pipline

    userid_results = db.readers.find().limit(50) # else too time consuming

    for doc in userid_results: # iterate over result and call next function for each iten
            pipelines.get_books_w_merge(doc["_id"])

    # reshape recommendations

    pipelines.reshape_recommendations()
    
    cursor = db.recommendations_reshaped.find() # gets data from the resulting collection

    df =  pd.DataFrame(list(cursor)) # construct the df for faster results and better accessebility

    return df # return dataframe as result

# inspect results

'''
get_recommendations("Tell Me This Isn't Happening")

recommendation_results = db.recommendations_reshaped.find().limit(5) # get frist 10 records (high rated)
df =  pd.DataFrame(list(recommendation_results)) # for faster results and better accessebility
print(df.iat[0,5])
'''
'''
for doc in recommendation_results: # get result and additional info
    rating = str ( doc["Rating"] )
    count = str ( doc["Count"] )
    isbn = doc["_id"]
    pprint.pprint( db.books.find_one({"ISBN":doc["_id"]})["Book_Title"]) 
    pprint.pprint( "Rating: " + rating + " / ISBN: " + isbn + " / Count: " + count)
'''
