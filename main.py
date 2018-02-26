#coding: utf-8
from FreeDriveClient import *

def main():
    client = FreeDriveClient()
    client.list_files(10)
    client.upload('testfile.txt')

if __name__ == '__main__':
    main()
