
import tkinter as tk
from pymongo import MongoClient
from tkinter import *
from tkinter import ttk
from tokenize import String
from matplotlib.pyplot import text
import pandas as pd

#imports for discplaying url images
from PIL import ImageTk,Image
import urllib.request 
from io import BytesIO
import requests


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
    '''
    get_recommendations(drop.get())

    # Make a query to the specific DB and Collection
    cursor = db.recommendations_reshaped.find()

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor)) # for faster results and better accessebility

    url = df.iat[0,6]
    print(url)
    url="http://images.amazon.com/images/P/0439095026.01.MZZZZZZZ.jpg"
    '''
    url="http://images.amazon.com/images/P/0439095026.01.MZZZZZZZ.jpg"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    image_1 = ImageTk.PhotoImage(Image.open(img))
    label = Label(image=image_1)
    label.image = image_1 # keep a reference!
    label.grid(row=3, sticky=W)


    for i in range(5):
        i+1 # skip first book = search input
        row = 2 + i
        #result_box (df.iat[i,1], df.iat[i,2], df.iat[i,3],df.iat[i,4], df.iat[i,5], df.iat[i,6], row, 2) 


def result_box(title, author, isbn, rating, count, url, row, column):

    # create labels
    book_info = Label(search_book, text= str(title) + "/n written by" + str(author))
    book_info.grid(row=row, column=column, padx=10)
    book_recomm = Label(search_book, text= "Has been rated " + str(rating) + " by " + str(count) + " other readers who also read your book")
    book_recomm.grid(row=(row), column=column, padx=10)

    #raw_data = urllib.request.urlopen(cover).read()
    #im = Image.open(io.BytesIO(raw_data))
    #image_1 = ImageTk.PhotoImage(Image.open("titelpic.jpeg"))
    #image_set = Label(image=image_1)
    #image_set.grid(row=6, sticky=W)


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
