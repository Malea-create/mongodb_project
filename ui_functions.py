import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd

#imports for discplaying url images
from PIL import ImageTk,Image
from io import BytesIO
import requests

import core_functions  # get algorightm

### User Interface Functions ###

'''

this file contents the functions to properly display the results in the user interface

therefore it includes:
- get_result() calls the algorightm on a user input and issues output of the result
- result_box() creates several widgets to display information for each resulr

'''

def get_result (search_book, input): # called by the button to initiate search

    # display input

    yoursearch = Label(search_book, text=input, wraplengt=180) # displays informations about searched item
    yoursearch.grid(row=2, column=2, padx=10)
    yoursearch_text = Label(search_book, text="You might also like: ", wraplengt=180)
    yoursearch_text.grid(row=2, column=0, padx=10)

    # get results

    try:
        df = core_functions.get_recommendations(input) # calls alorightm on the user input
    except:
        print("Sorry this title could't be found or there is not enough data for a recommendation.")
        print("Try another title!")

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
        result_box (search_book, df.iat[i,1], df.iat[i,2], df.iat[i,3],df.iat[i,4], df.iat[i,5], df.iat[i,6], row, col) 


def result_box(search_book, title, author, isbn, rating, count, url, row, column): # create a number of widgets for each result

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