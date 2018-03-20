#coding: utf-8
from FreeDriveClient import *
import sys


def main():
    path = str(sys.argv[1])

    backup_interval = int(sys.argv[2])
    last_backup = datetime.datetime.now()
    
    firstRun = int(sys.argv[3])
    client = FreeDriveClient()
    
    while 1:
        current_time = datetime.datetime.now()
        diff = current_time - last_backup
        if diff.days >= backup_interval or firstRun:
            backup_id = client.uploadFolder(path)
            last_backup = datetime.datetime.now()
            
            #Uploads log file
            client.upload(os.path.dirname(path) + "/backup.log", backup_id)
        
        firstRun = False        


if __name__ == '__main__':
    main()
