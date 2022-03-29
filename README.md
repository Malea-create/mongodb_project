# mongodb_project
Database Anaylsis using MongoDB

# About the Application
"Book Crossing is the library for the whole world". It tracks how a book is passed from reader to reader. 
Using this data, the application is able to make 5 recommendations depending on a book title that is given by you as the user. 
This takes into account which books have received a good rating from readers who also liked your selection.

The application is written in distributed python files. 
- "main" this is the only executable file to initiate a user interface and call the alrorightm
- "core_functions" calls functions from other files in order to get one function, that includes the program logic/alogrightm
- "pipelines" stores all aggregation pipelines for querieing and shaping the collections
- "setup_functions" stores all functions to properly create collections and check the result
- "ui_functions" contents the functions to properly display the results in the user interface

This guide will take you through the necessary steps to launch the application and use it successfully.

# File Structure and Arichtecture
After opening the zip file you will find next to this readme, a collection of files and a data folder
the only executable file is called main, it calls the functions in the other files.

![alt text](http://url/to/img.png)

# Starting Mongo DB
Enter the following commands in your virtual machine terminal to start the database:

  sudo systemctl start mongod 
  (start Mongo DB)

  sudo service mongod status
  (if started succesfully it should display: "Active: active (running)")

You can now close this terminal window and proceed to the next step

# Verify/Install needed Packeges
Please make sure that you have installed the following packages/versions and otherwise proceed with the offered download commands.

Check your python version:

  python3

The following is a description to download the packet manager pip to further install the needed liabries for python:

  sudo apt update
  (updating the package list)

  sudo apt install python3-pip
  (install pip for Python 3)

  pip3 --version
  (verify the installation by checking the pip version / should be pip 20.3.4)

Now you are ready to instell the packages needed to start the application:

  pip3 install tk
  pip3 install pymongo
  pip3 install pandas
  pip3 install PLC

# Execute Main
To start the application, please change to the directory where you saved the files (use dir/cd or for Mac ld/cd).
If you are in the mongodh_project folder, do the following:

  python 3 main.py
  (start application)


# Using the Application
The following steps will guide you through the application:

- Enter the title of your favorite book to find out which books were liked by those who also liked your selection.
- Press the search button to start the process 
- Do not press the search button twice, as it may take a few seconds for the result to appear due to the large amount of data
- 5 or less recommendations will be displayed 
- If your title was not found or no recommendations are possible - try with a new recommendation or restart the application before trying with a new recommendation
- You can repeat the search in the same window by deleting the title you searched for first and entering a new one (reloading the window may take a few seconds, so don't be bothered if the layout changes briefly - wait again)


For example, try searching for the following books:

Translated with www.DeepL.com/Translator (free version)
- Dating Big Bird
- Missing Susan
- Kitchen Privileges : A Memoir
- Daisy Fay and the Miracle Man
(you can find more booktitles in the BX-Books.csv in the data folder)
