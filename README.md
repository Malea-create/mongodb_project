# mongodb_project
Database Anaylsis using MongoDB

# File structure
after opening the zip-file or downloading the mongodb_project you find a collection of files and a data foulder alonside this readmy
the only executable file is named ... it will call to the functions in the other files.


# Starting Mongo DB

type the following commands into the terminal of your virtual maschine

sudo systemctl start mongod 
(start Mongo DB)

sudo service mongod status
(if started succesfully it should display: "Active: active (running)")

(to start/stop Mongo DB when needen (not now !) : sudo service mongod stop/restart )

you can now close this terminal window and move on to the next step

# Verify needed packeges

please make sure you have installed the following packages/versions and if not proceed with the provided download commands

try:
python3

The following is a description to download the packet manager pip to further install the needed liabries for python
Installing pip (packetmanager) for Python 3
Start by updating the package list using the following command: 
sudo apt update
Use the following command to install pip for Python 3: 
sudo apt install python3-pip
Once the installation is complete, verify the installation by checking the pip version: 
pip3 --version
sould be pip 20.3.4

- install
pip3 install tk
pip3 install pymongo
pip3 install pandas
pip3 install PLC

# Execute xy 

change directory to where you saved the files ( use dir/cd or for mac ld/cd)
when you are in the mongodh_project folder execute the following
python 3 filename
# network interfaces
net:
  port: 27017
  bindIp: 192.168.56.100
  sudo gedit /etc/mongod.conf

# Using the Application
- type in your favorite books title, in order to find out which books where liked by the ones who also liked your choice
- press the search button to start the process 
- do not press the search button twice, due to the large amount of data it will take a couple of secounds for the result to appear
- 5 or less recommendations are displayed (if not your title could not be found or no recommendations are possible - try a new one or restart the application before trying a new one)
- you can search again in the same window by deleting your first searched title and typing a new one (reloading the window can take a secound so dont be disturbed when the layout changes shortly - again please wait paitiantly)


For example try:
- Dating Big Bird
- Missing Susan
- Kitchen Privileges : A Memoir
- Daisy Fay and the Miracle Man
