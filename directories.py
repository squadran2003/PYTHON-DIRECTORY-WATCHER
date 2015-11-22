"""PY Directory watcher. This command line app monitors a specified directory for file creation,
when a file is created it runs the corresponding batchfile. The creation event only gets 
triggered when the files in the folder equals the trigger you specify for this directory, 
ie if you specified 2 files as a trigger, the batch file will only run when the there are 2 files
created in the directory."""

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
  The directory you are trying to delete does not exist
  as an argument and deletes that record from the database."""

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
    
  
  

  