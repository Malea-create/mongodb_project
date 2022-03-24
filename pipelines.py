import pymongo
from pymongo import MongoClient
import setup_functions
import pprint

# Establish connection with Mongo DB and create DB
client = MongoClient('mongodb://localhost:27017') # connect now to save db, ...
#pprint.pprint(client.list_database_names()) #see availible db

# Create DB in Mongo DB
db_name = 'BookCrossing_DB'
db = client[db_name] # Creating a database


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
'''
    result = db.readers.find()
    for doc in result:
        pprint.pprint( doc )

    pprint.pprint( db.readers.count_documents({}) )
'''

##### get all books (isbns) form readers ####

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
'''
    result = db.recommendations.find()
    for doc in result:
        pprint.pprint( doc )

    pprint.pprint( db.recommendations.count_documents({}) )
'''

def reshape_recommendations(isbn):

    reshape_pipline = [ # pipline = array of multiple elements

                { # match processing stage 
                    "$match": # equal to find
                    {'ISBN': {'$ne': isbn}} #{ "$ne": ["ISBN",isbn] } 
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
                { # limit output
                    "$limit" : 10 },
                {"$lookup":
                    {
                    "from": "books",
                    "localField": "_id",
                    "foreignField": "ISBN",
                    "as": "book_info"
                    }
                },
                { "$project": 
                    {
                    "Title": "$book_info.Book_Title",
                    "Author": "$book_info.Book_Author",
                    "ISBN": "$_id", 
                    "Rating": "$Rating",     
                    "Count": "$Count", 
                    "Image_URL": "$book_info.Image_URL_M",   
                    }
                },
                { # out processing stage 
                    "$out":"recommendations_reshaped"
                }
            ]    

    db.recommendations.aggregate(reshape_pipline) # use pipeline

    # inspect results
    '''    
        result = db.recommendations_reshaped.find()
        for doc in result:
            pprint.pprint (doc)
    '''
    
