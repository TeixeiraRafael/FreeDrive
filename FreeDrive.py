#coding: utf-8
from FreeDriveClient import *
import sys


def main():
    print("Google Drive backup tool started.\n")

    path = str(sys.argv[1])
    backup_interval = int(sys.argv[2])
    last_backup = datetime.datetime.now()
    firstRun = True
    client = FreeDriveClient()
    
    while 1:
        current_time = datetime.datetime.now()
        diff = current_time - last_backup
        if diff.days >= backup_interval or firstRun:
            backup_id = client.uploadFolder(path)
            last_backup = datetime.datetime.now()
            print(os.path.dirname(path))
            #Uploads log file
            client.upload(os.path.dirname(path) + "/backup.log", backup_id)
            print("Done!")
            

        firstRun = False        


if __name__ == '__main__':
    main()
