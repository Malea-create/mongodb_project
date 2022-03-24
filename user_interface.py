
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

def get_result (): # called by the button to initiate search

    # display input

    yoursearch = Label(search_book, text=drop.get()) # displays informations about searched item
    yoursearch.grid(row=2, column=2, padx=10)
    yoursearch_text = Label(search_book, text="Your search: ")
    yoursearch_text.grid(row=2, column=1, padx=10)

    # get results

    get_recommendations(drop.get()) # calls alorightm on the user input

    cursor = db.recommendations_reshaped.find() # gets data from the resulting collection

    df =  pd.DataFrame(list(cursor)) # construct the df for faster results and better accessebility

    # display results

    book_info = Label(search_book, text = "written by " + str(df.iat[0,2])) # further information on the input
    book_info.grid(row=3, column=2, padx=10)
    book_recomm = Label(search_book, text= "Rated " + str(int(df.iat[0,4])) + " by " + str(df.iat[0,5]) + " users")
    book_recomm.grid(row=(4), column=2, padx=10)

    url="http://images.amazon.com/images/P/0439095026.01.MZZZZZZZ.jpg" # df.iat[0,6] # cover of the input
    response = requests.get(url)
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

    url = "http://images.amazon.com/images/P/0439095026.01.MZZZZZZZ.jpg"

    # create cover image 

    response = requests.get(url) # read url
    image_1 = ImageTk.PhotoImage(Image.open(BytesIO(response.content))) # creat instance of ImageTK
    label = Label(image=image_1)
    label.image = image_1 # keep a reference
    label.grid(row=row, column=column) # put to grif

    row=row+1 # display next item in new row

    book_info = Label(search_book, text= str(title)) # add info about title
    book_info.grid(row=row, column=column, padx=10)

    row=row+1

    book_info = Label(search_book, text = "written by" + str(author)) # add info about author
    book_info.grid(row=row, column=column, padx=10)

    row=row+1

    book_recomm = Label(search_book, text= "Rated " + str(int(rating)) + " by " + str(count) + " users") # add info about rating and counting
    book_recomm.grid(row=(row), column=column, padx=10)

    


options = ["Tell Me This Isn't Happening", "New Vegetarian: Bold and Beautiful Recipes for Every Occasion"]

# Main Layout of Grid

# Label
search_box_label = Label(search_book, text="Search for Book")
search_box_label.grid(row=0, column=0, padx=10, pady=10)

# Button
search_button = Button(search_book, text="Search now", command= get_result)
search_button.grid(row=0, column=2, padx=10)

# Drop Down Box
drop = ttk.Combobox(search_book, values = options)
drop.current(0) # default
drop.grid(row=0, column=1, padx=10)

search_book.mainloop() # start displaying window and widgets
