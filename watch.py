from batch_file_monitor import BatchFileMonitor
import sys


while True:
    batch_file_path=input("Where is your batch file located? eg yourpath\\bactfile.bat ?? ")
    path=input("Enter the path to the directory you would like to monitor! ")
    jobname=input(" Your Job Name ?  ")
    watcher=BatchFileMonitor(jobname,path,batch_file_path)
    watcher.watch()
    new_dir=input(" New Directory to Watch y for yes n for no??")
    if new_dir.lower()=='n':
        break     
    else:
        continue
        
         
                  