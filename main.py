#coding: utf-8
from FreeDriveClient import *

def main():    
    path = str(input())

    client = FreeDriveClient()
    client.uploadFolder(path)

    print("Done!")
            
if __name__ == '__main__':
    main()
