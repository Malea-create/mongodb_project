
import tkinter as tk
from pymongo import MongoClient
from tkinter import *
from tkinter import ttk
import pandas as pd

#imports for discplaying url images
from PIL import ImageTk,Image
import urllib.request 
from io import BytesIO
import requests


from core import get_recommendations # get algorightm

### User Interface ###

'''

this is the only executable file to initiate a user interface and call the alrorightm

therefore it includes:
- layout of user interface
- get_result() calls the algorightm on a user input and issues output of the result
- result_box() creates several widgets to display information for each resulr

'''

# Establish connection with Mongo DB and create DB
client = MongoClient('mongodb://localhost:27017') # connect now to save db, ...
#pprint.pprint(client.list_database_names()) #see availible db

# Create DB in Mongo DB
db_name = 'BookCrossing_DB'
db = client[db_name] # Creating a database

# Search book window

search_book = Tk() 
search_book.title("Book Recommendor")
search_book.iconbitmap('data/bookicon.jpg')

def get_result (): # called by the button to initiate search

    # display input

    yoursearch = Label(search_book, text=drop.get(), wraplengt=180) # displays informations about searched item
    yoursearch.grid(row=2, column=2, padx=10)
    yoursearch_text = Label(search_book, text="You might also like: ", wraplengt=180)
    yoursearch_text.grid(row=2, column=0, padx=10)

    # get results

    get_recommendations(drop.get()) # calls alorightm on the user input

    cursor = db.recommendations_reshaped.find() # gets data from the resulting collection

    df =  pd.DataFrame(list(cursor)) # construct the df for faster results and better accessebility

    # display results

    book_info = Label(search_book, text = "written by " + str(df.iat[0,2][0]), wraplengt=180) # further information on the input
    book_info.grid(row=3, column=2, padx=10)
    book_recomm = Label(search_book, text= "Rated " + str(int(df.iat[0,4])) + " by " + str(df.iat[0,5]) + " users", wraplengt=180)
    book_recomm.grid(row=(4), column=2, padx=10)

    url= df.iat[0,6] # cover of the input
    response = requests.get(url[0])
    image_1 = ImageTk.PhotoImage(Image.open(BytesIO(response.content)))
    label = Label(image=image_1)
    label.image = image_1 # keep a reference!
    label.grid(row=1,column=2)

    for i in range(5): # create result_box for each result item/ call df to pass parameters 
        row = 5
        col = i
        i = i + 1 # skip first book = search input
        result_box (df.iat[i,1], df.iat[i,2], df.iat[i,3],df.iat[i,4], df.iat[i,5], df.iat[i,6], row, col) 


def result_box(title, author, isbn, rating, count, url, row, column): # create a number of widgets for each result

    # create cover image 

    response = requests.get(url[0]) # read url
    image_1 = ImageTk.PhotoImage(Image.open(BytesIO(response.content))) # creat instance of ImageTK
    label = Label(image=image_1)
    label.image = image_1 # keep a reference
    label.grid(row=row, column=column) # put to grif

    row=row+1 # display next item in new row

    book_info = Label(search_book, text= str(title[0]), wraplengt=180) # add info about title
    book_info.grid(row=row, column=column, padx=10)

    row=row+1

    book_info = Label(search_book, text = "written by " + str(author[0]), wraplengt=180) # add info about author
    book_info.grid(row=row, column=column, padx=10)

    row=row+1

    book_recomm = Label(search_book, text= "Rated " + str(int(rating)) + " by " + str(count) + " users", wraplengt=180) # add info about rating and counting
    book_recomm.grid(row=(row), column=column, padx=10)

    
def get_first_result ():

    get_result()
    first_search_button.destroy()
    secound_search_button.grid(row=0, column=2, padx=10)

def get_more_result ():

    #get_result()
    
    for child in search_book.children.values():
        child.grid_forget()
    
    search_box_label.grid(row=0, column=0, padx=10, pady=10)
    secound_search_button.grid(row=0, column=2, padx=10)
    drop.grid(row=0, column=1, padx=10)


# Main Layout of Grid

# Label
search_box_label = Label(search_book, text="Tell me which book you liked: ")
search_box_label.grid(row=0, column=0, padx=10, pady=10)

# Button
first_search_button = Button(search_book, text="Search for other books you might like", command= get_first_result)
first_search_button.grid(row=0, column=2, padx=10)

secound_search_button = Button(search_book, text="Search again ", command= lambda:[get_more_result(), get_result()])

drop = tk.Entry(search_book)
drop.grid(row=0, column=1, padx=10)

search_book.mainloop() # start displaying window and widgets
