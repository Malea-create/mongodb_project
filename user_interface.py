import tkinter as tk
from urllib import request
from matplotlib import image
import pymongo
from pymongo import MongoClient
from tkinter import *
from tkinter import ttk
from tokenize import String
from matplotlib.pyplot import text


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

    result = get_recommendations(drop.get())

    myLabel = Label(search_book, text=result[1])
    myLabel.grid(row=3, column=2, padx=10)

    myLabel = Label(search_book, text=result[2])
    myLabel.grid(row=4, column=2, padx=10)

    myLabel = Label(search_book, text=result[3])
    myLabel.grid(row=5, column=2, padx=10)

    myLabel = Label(search_book, text=result[4])
    myLabel.grid(row=6, column=2, padx=10)

    myLabel = Label(search_book, text=result[5])
    myLabel.grid(row=7, column=2, padx=10)
    
    '''
    image_url = "http://images.amazon.com/images/P/0439095026.01.MZZZZZZZ.jpg" #doc["Image_URL_M"]
    title = "Titel"#str ( doc["Book_Title"])
    author = "Author"#str ( doc["Book_Author"])
    result_box(image_url, title, author,3,2)

    for doc in result:
            # def parameter 
        image_url = "http://images.amazon.com/images/P/0439095026.01.MZZZZZZZ.jpg" #doc["Image_URL_M"]
        title = "Titel"#str ( doc["Book_Title"])
        author = "Author"#str ( doc["Book_Author"])
        print (image_url, title, author)
        #rating = db.recommendations_reshaped.find_one({"_id":result})["Rating"]
        #count = db.recommendations_reshaped.find_one({"_id":result})["Count"]

        result_box(image_url, title, author,3,2)
        '''
        
    
'''
def result_box(image_url, title, author, row, column):

    # create labels
    book_info = Label(search_book, text= title + "/n written by" + author)
    book_info.grid(row=row, column=column, padx=10)
    #book_recomm = Label(search_book, text= "Rated:" + rating + " Read by:" + count + " others")
    #book_recomm.grid(row=row, column=column, padx=10)

    # add image
    response = requests.get(image_url)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    panel = tk.Label(search_book, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
'''

options = ["Tell Me This Isn't Happening", "New Vegetarian: Bold and Beautiful Recipes for Every Occasion"]

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
