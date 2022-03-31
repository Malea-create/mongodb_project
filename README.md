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

The application will connect to the databse in Atlas MongoDb. Mongo Db runs on the AWS.
The following figure depicts the interaction and dataflow of between user, GUI, application, database, and the cloud.

![alt text](https://github.com/Malea-create/mongodb_project/blob/ba12f84c9c54b88a4b26d35a18cf9dd4c84073e8/docu/MongoDb_Architecture.png?raw=true)


# Verify/Install needed Packeges
Please make sure that you have installed the following packages/versions and otherwise proceed with the offered download commands.

Check your python version:

  python3
  (it should be 3.9.10)

The following is a description to download the packet manager pip to further install the needed liabries for python:

  sudo apt update
  (updating the package list)

  sudo apt install python3-pip
  (install pip for Python 3)

  pip3 --version
  (verify the installation by checking the pip version / should be pip 20.3.4)

Now you are ready to install the packages needed to start the application:

 - pip3 install tk
 - pip3 install pymongo
 - pip3 install pandas
 - pip3 install PLC
 - pip3 install dnspython

For Ubuntu you need to add:

-sudo apt-get install python3-pil python3-pil.imagetk
-sudo apt-get install python3-tk

(you might need to change the commands slightly according to your operation system)

# Execute Main
To start the application, please change to the directory where you saved the files (use dir/cd or for Mac ld/cd).
If you are in the mongodh_project folder, do the following:

  python 3 main.py
  (start application)


# Using the Application
The following steps will guide you through the application:

- Enter the title of your favorite book to find out which books were liked by those who also liked your selection.

For example, try searching for the following books:

Translated with www.DeepL.com/Translator (free version)
- Tell Me This Isn't Happening
- Missing Susan
- Kitchen Privileges : A Memoir
- Dating Big Bird
- Daisy Fay and the Miracle Man
(you can find more booktitles in the BX-Books.csv in the data folder)

- Press the search button to start the process 
- Do not press the search button twice, as it may take a few seconds for the result to appear due to the large amount of data and the performance of TKinter
- 5 or less recommendations will be displayed 
- You can repeat the search in the same window by deleting the title you searched for first and entering a new one (reloading the window may take a few seconds, so don't be bothered if the layout changes briefly - please wait patiently)
- When you want to restart the application you have to close the window first 

# Trouble Shooting 
before continuing with the different error handling concepts 
- check if all packages are properly installed and the right python version is in place! (versions and installation instructions can be found above)
LEVEL 1 ERROR:
- If your title is not found, no recommendations are possible and only your title is displayed in the window - try a new title!
Level 2 ERROR:
- The concept of exception handling helps to understand the source of error when the message "Sorry this title couldn't be found or there is not enough data for a recommendation" appears, something went wrong within the algorithm.
Sorry about that, please try a new title!
Level 3 ERROR:
- If none of the above apply: restart the application before trying with a new recommendation, or check the command line for further instructions
(reach out to developer if needed)
