import tkinter as tk
from tkinter import *

import ui_functions

### User Interface ###

'''

this is the only executable file to initiate a user interface and call the alrorightm

therefore it includes:
- layout of user interface
- get_result() calls the algorightm on a user input and issues output of the result
- result_box() creates several widgets to display information for each resulr

'''

# Search book window

search_book = Tk() 
search_book.title("Book Recommendor")
search_book.iconbitmap('data/bookicon.jpg')

    
def get_first_result ():

    input = drop.get()

    print("You are searching for recommendations for the following title: "+input) # communicate with user

    secound_search_button.grid(row=0, column=2, padx=10)
    first_search_button.destroy()

    ui_functions.get_result(search_book, input)


    

def get_more_results ():

    input = drop.get()

    print("You are searching for recommendations for the following title: "+input) # communicate with user
   
    for child in search_book.children.values():
        child.grid_forget()
    
    search_box_label.grid(row=0, column=0, padx=10, pady=10)
    secound_search_button.grid(row=0, column=2, padx=10)
    drop.grid(row=0, column=1, padx=10)

    ui_functions.get_result(search_book, input)



# Main Layout of Grid

# Label
search_box_label = Label(search_book, text="Tell me which book you liked: ")
search_box_label.grid(row=0, column=0, padx=10, pady=10)

# Button
first_search_button = Button(search_book, text="Search for other books you might like", command= get_first_result)
first_search_button.grid(row=0, column=2, padx=10)

secound_search_button = Button(search_book, text="Search again ", command= get_more_results)

drop = tk.Entry(search_book)
drop.grid(row=0, column=1, padx=10)

search_book.mainloop() # start displaying window and widgets
