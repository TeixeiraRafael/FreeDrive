#coding: utf-8
from FreeDriveClient import *
import sys


def main():

    print("Google Drive backup tool stated.")

    path = str(sys.argv[1])
    backup_interval = int(sys.argv[2])
    last_backup = datetime.datetime.now()
    
    while 1:
        current_time = datetime.datetime.now()
        diff = current_time - last_backup
        if(diff.days > backup_interval):
            client = FreeDriveClient()
            client.uploadFolder(path)
            last_backup = datetime.datetime.now()
            print("\nBackup successfully finished at " + last_backup.strftime('%d-%m-%Y %H:%M:%S') + "\n")



if __name__ == '__main__':
    main()
