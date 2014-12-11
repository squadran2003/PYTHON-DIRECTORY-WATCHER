import sys, os
import subprocess
from subprocess import Popen,PIPE
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class BatchFileMonitor(FileSystemEventHandler):
    
    jobname="" # your job name
    dir_name="" # directory you want to watch 
    batch_file_path="" # path to your batch file location
    
    def on_created(self, event):
        list_of_file_in_drectory=os.listdir(self.dir_name)
        if(len(list_of_file_in_drectory)>5):  #check to see how many files in the directory and then call batch file when the desired no of files have been created
            p = subprocess.Popen(self.batch_file_path, creationflags=subprocess.CREATE_NEW_CONSOLE)# executing the batch file 
    
    def __init__(self,jobname,dir_name,batch_file_path):
        self.jobname=jobname
        self.dir_name=dir_name
        self.batch_file_path=batch_file_path
            
    
    def watch(self):
         observer = Observer()
         event_handler = self
         observer.start()
         print('MONITORING YOUR {} DIRECTORY ...'.format(self.dir_name))
         observer.schedule(event_handler,self.dir_name, recursive=False)
         try:
            while True:
                time.sleep(1)
         except KeyboardInterrupt:
             observer.stop()
         observer.join()