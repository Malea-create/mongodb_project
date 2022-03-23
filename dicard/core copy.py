import pymongo
from pymongo import MongoClient
import setup_functions
import pprint

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

'''
# Create collections for each csv file 

setup_functions.add_collection_to_db('data/BX-Book-Ratings.csv', db, 'book_ratings') # pass csv file path and collection name 
setup_functions.add_collection_to_db('data/BX-Books.csv', db, 'books') # pass csv file path and collection name 
setup_functions.add_collection_to_db('data/BX-Users.csv', db, 'user') # pass csv file path and collection name 
setup_functions.show_collections(db, db_name)
'''

##### get ISBN from search ####

def get_isbn (booktitle):

    isbn_pipline = [ # pipline = array of multiple elements

        { # match processing stage 
            "$match": # equal to find
            { "Book_Title":booktitle } # value/ querie
        },
        { # group processing stage 
            "$group":
            {"_id":"$ISBN"}
        },
        { # out processing stage 
            "$out":"isbns"
        }
    ]

    db.books.aggregate(isbn_pipline) # use pipeline

    # inspect results

    result = db.isbns.find()
    for doc in result:
        pprint.pprint( doc )

    pprint.pprint( db.isbns.count_documents({}) )


##### get readers for isbn ####

def get_userids (isbn):

    users_pipline = [ # pipline = array of multiple elements

            { # match processing stage 
                "$match": # equal to find
                { "ISBN":isbn } # value/ querie
            },
            { # group processing stage 
                "$group":
                {"_id":"$UserID"} # get rid of any users who read book twice
            },
            { # out processing stage 
                "$out":"readers"
            }
        ]

    db.book_ratings.aggregate(users_pipline) # use pipeline

    # inspect results

    result = db.readers.find()
    for doc in result:
        pprint.pprint( doc )

    pprint.pprint( db.readers.count_documents({}) )


##### get all books (isbns) form readers ####

def get_books (userid): # input needs to be integer / eles none / starting w/o 0 - > int

    book_pipline = [ # pipline = array of multiple elements

            { # match processing stage 
                "$match": # equal to find
                { "UserID":userid } # value/ querie + max
            },
            { # group processing stage 
                "$group":
                { "_id":"$ISBN", # get rid of dublicates
                "Rating":{ "$avg": "$BookRating" } # calc average rating 
                }
            },
            { # sort processing stage 
                "$sort": 
                { "Rating" : -1 } 
            },
            { # match processing stage 
                "$match": # equal to find
                { "Rating": {"$gt": 0} } # drop everything that is rated 0 (see if we need that)
            },
            { # out processing stage 
                "$out":"recommendations"
            }
        ]

    db.book_ratings.aggregate(book_pipline) # use pipeline

    # inspect results

    result = db.recommendations.find()
    for doc in result:
        pprint.pprint( doc )

    pprint.pprint( db.recommendations.count_documents({}) )

# Problem: save data in same collection 
# 1) use merge and put data into same collection
# 2) use out and merge different collections afterwards

def get_books_w_merge (userid): # input needs to be integer / eles none / starting w/o 0 - > int

    book_pipline = [ # pipline = array of multiple elements

            { # match processing stage 
                "$match": # equal to find
                { "UserID":userid  }  # value/ querie 
            },
            { 
                "$merge": 
                {"into": "recommendations",
                "whenMatched": "keepExisting", 
                "whenNotMatched": "insert"  }
            }
        ]

    db.book_ratings.aggregate(book_pipline) # use pipeline

    # inspect results

    result = db.recommendations.find()
    for doc in result:
        pprint.pprint( doc )

    pprint.pprint( db.recommendations.count_documents({}) )


### ACTION ###

def get_recommendations(user_input):

    db.recommendations.drop() # needs to be emptied every time (storage for new results)
    get_isbn(user_input) # start Process

    # pass isbn results to next pipline

    isbn_results = db.isbns.find()
    for doc in isbn_results:
            get_userids(doc["_id"])
            isbn = doc

    # pass user results to next pipline

    userid_results = db.readers.find().limit(50) # else too time consuming
    for doc in userid_results:
            get_books_w_merge(doc["_id"])

    # reshape recommendations

    reshape_pipline = [ # pipline = array of multiple elements

                { # match processing stage 
                    "$match": # equal to find
                    { "_id": { "$ne": isbn } } 
                },
                { # group processing stage 
                    "$group":
                    { "_id":"$ISBN", # get rid of dublicates
                    "Count":{ "$count": {}},
                    "Rating":{ "$avg": "$BookRating" } # calc average rating 
                    }
                },
                { # sort processing stage 
                    "$sort": 
                    { "Count" : -1,"Rating" : -1 } 
                },
                { # out processing stage 
                    "$out":"recommendations_reshaped"
                }
            ]


    db.recommendations.aggregate(reshape_pipline) # use pipeline
    db.recommendations_reshaped.delete_one({"_id": isbn}) # why is this not working ?!
    result = db.recommendations_reshaped.find()
    for doc in result:
        pprint.pprint (doc)

    # get top 5 out of the recommendation collection

    recommendation_results = db.recommendations_reshaped.find().limit(5) # get frist 10 records (high rated)
    top5_results = []
    for doc in recommendation_results:
        top5_results.append(doc["_id"])
    
    return top5_results

    #for doc in recommendation_results: # get result and additional info
            #rating = str ( doc["Rating"] )
           # count = str ( doc["Count"] )
           # isbn = doc["_id"]
           # pprint.pprint( db.books.find_one({"ISBN":doc["_id"]})["Book_Title"]) 
           # pprint.pprint( "Rating: " + rating + " / ISBN: " + isbn + " / Count: " + count)
