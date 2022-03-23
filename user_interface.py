import tkinter as tk
from urllib import request
from matplotlib import image
from pymongo import MongoClient
from tkinter import *
from tkinter import ttk
from tokenize import String
from matplotlib.pyplot import text
import pandas as pd


from core import get_recommendations # get logic

# Establish connection with Mongo DB and create DB
client = MongoClient('mongodb://localhost:27017') # connect now to save db, ...
#pprint.pprint(client.list_database_names()) #see availible db

# Create DB in Mongo DB
db_name = 'BookCrossing_DB'
db = client[db_name] # Creating a database

# Search book

search_book = Tk()
search_book.title("Book Recommendor")

def get_result ():

    myLabel = Label(search_book, text=drop.get())
    myLabel.grid(row=1, column=2, padx=10)

    get_recommendations(drop.get())

    # Make a query to the specific DB and Collection
    cursor = db.recommendations_reshaped.find()

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor)) # for faster results and better accessebility

    for i in range(5):
        row = 2 + i
        result_box (df.iat[i,0], df.iat[i,1], df.iat[i,2], row, 2) # check result


def result_box(isbn, rating, count, row, column):

    # create labels
    #book_info = Label(search_book, text= title + "/n written by" + author)
    #book_info.grid(row=row, column=column, padx=10)
    book_recomm = Label(search_book, text= "Has been rated " + str(rating) + " by " + str(count) + " other readers who also read your book")
    book_recomm.grid(row=row, column=column, padx=10)

    '''
    # add image
    response = requests.get(image_url)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    panel = tk.Label(search_book, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    '''


options = ["Tell Me This Isn't Happening", "New Vegetarian: Bold and Beautiful Recipes for Every Occasion"]

# Layout of Grid

# Label
search_box_label = Label(search_book, text="Search for Book")
search_box_label.grid(row=0, column=0, padx=10, pady=10)
# Button
search_button = Button(search_book, text="Search now", command= get_result)
search_button.grid(row=1, column=0, padx=10)

# Drop Down Box
drop = ttk.Combobox(search_book, values = options)
drop.current(0) # default
drop.grid(row=0, column=2, padx=10)

search_book.mainloop()
