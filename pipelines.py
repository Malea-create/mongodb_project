import pymongo
from pymongo import MongoClient
import setup_functions
import pprint


### Piplines ###

'''

this file stores all aggregation pipelines for querieing and shaping the collections

Therefore it includes:
- get_isbn pipelines() gets matching isbn to the user input from the books collection and saves in in new collection called isbns
- get_userids pipeline() gets matching userIDs from the users collection according to the isbn input and saves it in new collection called readers
- get_books_w_merge pipeline() gets all isbns from the book_rating collection witch match the userID input and saves it in new collection called recommendations
- reshape_recommendations() pipline reshapes collection input by grouping and counting the isbns 

'''

# Establish connection with Mongo DB and create DB
client = MongoClient('mongodb://localhost:27017') # connect now to save db
#pprint.pprint(client.list_database_names()) #see availible db

# Create DB in Mongo DB
db_name = 'BookCrossing_DB'
db = client[db_name] # creating a database


#### get ISBN matching to user input ####

def get_isbn (booktitle):

    isbn_pipline = [ # pipline = array of multiple elements

        { # match processing stage 
            "$match": # equal to find
            { "Book_Title":booktitle } # value/ querie
        },
        { # group processing stage 
            "$group":
            {"_id":"$ISBN"} # group by ISBN
        },
        { # out processing stage 
            "$out":"isbns" # save documents in new collection
        }
    ]

    db.books.aggregate(isbn_pipline) # use pipeline on collection


#### get readers how read a specific isbn ####

def get_userids (isbn):

    users_pipline = [ # pipline = array of multiple elements

            { # match processing stage 
                "$match": # equal to find
                { "ISBN":isbn }, # value/ querie
            },

            { # group processing stage 
                "$group":
                {"_id":"$UserID", # get rid of any users who read book twice
                "Rating":{ "$avg": "$BookRating" } }
            },
            { # match processing stage 
                "$match": # equal to find
                { 'Rating': {'$gt': 4} }, # value/ querie
            },
            { # out processing stage 
                "$out":"readers" # save documents in new collection
            }
        ]

    db.book_ratings.aggregate(users_pipline) # use pipeline on collection

    # inspect results
    '''  

    result = db.readers.find()
    for doc in result:
        pprint.pprint( doc )

    pprint.pprint( db.readers.count_documents({}) )
    '''


#### get all books (isbns) which are read by specific userIDS ####

def get_books_w_merge (userid): # reminder: input needs to be integer / eles none / starting w/o 0 - > int

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
                # merge creates new collection and adds content each time it is called
            }
        ]

    db.book_ratings.aggregate(book_pipline) # use pipeline on collection

    # inspect results
'''
    result = db.recommendations.find()
    for doc in result:
        pprint.pprint( doc )

    pprint.pprint( db.recommendations.count_documents({}) )
'''

def reshape_recommendations():

    reshape_pipline = [ # pipline = array of multiple elements

                { # group processing stage 
                    "$group":
                    { "_id":"$ISBN", # get rid of dublicates
                    "Count":{ "$count": {}}, # count items which are grouped
                    "Rating":{ "$avg": "$BookRating" } # calculate average rating 
                    }
                },
                { # match processing stage 
                    "$match": # equal to find
                    {'Rating': {'$gt': 4}} # get all good ratings
                },
                { # sort processing stage 
                    "$sort": 
                    { "Count" : -1,"Rating" : -1 } # sort by count descending, then be rating descending
                },
                { # limit processing stage
                    "$limit" : 10 # limit output (we dont need more recommendations)
                },
                { # lookup processing stage equal to left side join
                    "$lookup":
                        {
                        "from": "books", # collection to join with
                        "localField": "_id", # key for joining in local collection
                        "foreignField": "ISBN", # key for joining in foreign collection
                        "as": "book_info" # save new items in column namen ...
                        }
                },
                { # projection processing stage 
                    "$project": 
                        {
                        "Title": "$book_info.Book_Title", # make new columns for each nested item
                        "Author": "$book_info.Book_Author",
                        "ISBN": "$_id", 
                        "Rating": "$Rating", # name items to keep them in document
                        "Count": "$Count", 
                        "Image_URL": "$book_info.Image_URL_M",   
                        }
                },
                { # out processing stage 
                    "$out":"recommendations_reshaped" # save documents in collection
                }
            ]    

    db.recommendations.aggregate(reshape_pipline) # use pipeline on collection

    # inspect results
    '''    
        result = db.recommendations_reshaped.find()
        for doc in result:
            pprint.pprint (doc)
    '''
    
