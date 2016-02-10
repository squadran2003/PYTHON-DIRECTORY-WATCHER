PYTHON-DIRECTORY-WATCHER
========================


#### Description:

Python-Directory-Watcher is a command line python app that monitors a specified directory for file created events,when the correct number of files get created in a directory an event is raised which runs a specified batch file.The app works well in the windows enviroments primary due to permission issues on other OS like linux or mac. The app uses a backend Sqlite3 database
to store information about the directories that need to be monitored.


#### Example:

```python


from peewee import *
from mywatchdog import *

db = SqliteDatabase('directories.db')

loopCount = 0

class Directory(Model):
  monitorDirectory = CharField(max_length=500,unique=True)
  batchFileDirectory = CharField(max_length=500)
  fileTrigger = IntegerField(null=False)
  
  class Meta:
    database = db


def manageInput(mystring):
  """This function takes a string and depending on the version of 
  python calls either raw_input or input function."""
  try:
    myInput = raw_input(mystring)
  except:
    myInput = input(mystring)
  return myInput      


def add_directories(my_dir,my_batchfile_path,trigger):
  """This function takes 3 arguments, The directory to monitor,the batchfilepath, 
  and the trigger( or the number of files that need 
  to be created before the batchfile runs)""" 

  try:
    Directory.create(monitorDirectory=my_dir
      ,batchFileDirectory=my_batchfile_path,fileTrigger=trigger)
    return " \n Directory added"
  except IntegrityError:
    directory = Directory.get(monitorDirectory=my_dir)
    directory.batchFile = my_batchfile_path
    directory.fileTrigger= trigger
    directory.save()
    return "\n Directory saved"


def list_directories():
  print("\n *** LIST OF DIRECTORIES BEING WATCHED \n")
  if Directory.select().count()==0:
    print("No directories being monitored !!")
  else:
    for dir in Directory.select():
      print("\n {} {} {}".format(dir.id,dir.monitorDirectory,dir.fileTrigger))


def del_directories(my_id):
    """This function takes an id or Primary key 
  and deletes that record from the database."""

  print("\n")
  try:
    directory = Directory.get(Directory.id == my_id)
    directory.delete_instance()
    print("\n")
    return "The Directory has been deleted! "
  except Directory.DoesNotExist:
    return "The directory you are trying to delete does not exist"  


  
         
         

def show_menu():

  mystring ="TO ADD A DIRECTORY [A] \n"
  mystring+="TO DELETE A DIRECTORY FROM THE QUEUE [D] \n"
  mystring+="TO START MONITORINING DIRECTORIES [M]\n"
  mystring+="TO LIST DIRECTORIES [L],\n"
  mystring+="TO QUIT [Q] \n"
  print(mystring)     



if __name__ == '__main__':
  db.connect()
  db.create_tables([Directory],safe=True)

  while True:
    if loopCount == 0:
      print(" \n WELCOME TO PY-DIRECTORY-WATCHER.\n")
    loopCount+=1  
    print("\n")
    show_menu()
    user_input = manageInput(">>  ")
    if user_input.lower()=="q":
      break;
    if user_input.lower()=="a":
      mydir = manageInput("PATH TO YOU DIRECTORY \n ")
      batchfilepath = manageInput("PATH TO THE BATCH FILE INCLUDING THE FILENAME AND EXTENTION \n") 
      fileTrigger = 0
      fileTrigger = int(manageInput("No of files for automation trigger ! >>  "))
      if mydir == "" or batchfilepath =="" or fileTrigger==0:
        print("PLEASE ENTER INFORMATION PROPERLY!!")
      else:
        print(add_directories(mydir,batchfilepath,fileTrigger))  
      continue
    if user_input.lower()=="l":
      list_directories() 
      continue 
    if user_input.lower()=="m":
      try:
        directory = Directory.select()   # getting all the directories in the database
        mywatcher = Watcher(directory)   # passing the returned select object to the Watcher class
        mywatcher.watch()
      except Exception as e:
        print(str(e))
      continue  
    if user_input.lower()=="d":
      id = 0
      id = int(manageInput("What is the Id of the directory >>  "))
      if id==0:
        print("You have not supplied a directory !")
      else:
        print(del_directories(id))       
    else:
      print(" \n SORRY DID NOT RECOGNISE YOUR INPUT >>")
      continue 

```      


#### Motivation:

Professionally I work as a data programmer, the idea for this app came from the need to automate some of my jobs at work. I set a directory to be monitored by the app,when the
data processing software exports data to a directory with the correct number of files a batch file gets called running another application which creates print ready pdf's.

#### Installation:

[] Download the zip or clone the repo
[] Install watchdog with the command pip install watchdog 
[] Install peewee pip install peewee 

#### Reference:

[] [WatchDog] (https://pypi.python.org/pypi/watchdog)  
[] [Peewee] (http://docs.peewee-orm.com/en/latest/)












