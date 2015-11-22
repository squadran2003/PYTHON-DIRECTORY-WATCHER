#!/usr/bin/python
import time,os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess



class Watcher(FileSystemEventHandler):

    directories = []
    event = None

    def __init__(self,directory_object):  # the directory object is a peewee return select object
        for directory in directory_object:  # creating a dictionary from the records saved in the database
            self.directories.append({"directory":directory.monitorDirectory,
                                     "batchfilepath":directory.batchFileDirectory,
                                     "fileTrigger":directory.fileTrigger, })
        self.event = self # setting the event as the current instance
        

    def on_created(self,event):
        currentdir = os.path.dirname(event.src_path) # getting the current directory from the on_created event
        for my_dict in self.directories:
            if my_dict["directory"]== currentdir:# check if the directory is the current directory from which the on_created event is raised
                filesInDir = os.listdir(currentdir) # getting a list of files in the current directory
                if "Thumbs.db" in filesInDir:  # removing any thumb.db files. This is applicable to windows 
                    filesInDir.remove("Thumbs.db")
                filelength = len(filesInDir)  # getting the no of files in the directory
                trigger = my_dict["fileTrigger"] # getting the trigger supplied for this directory
                if filelength == trigger: # if the trigger supplied or this directory is the same as the no of files in the directory then run the batch file
                    p = subprocess.Popen(my_dict["batchfilepath"], shell=True, stdout = subprocess.PIPE)
                    


    def watch(self):
        event_handler = self.event
        observer = Observer()
        for my_dict in self.directories:   # looping through the list to get each dictionary
            observer.schedule(event_handler, path=my_dict["directory"], recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()