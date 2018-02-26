#coding: utf-8
from FreeDriveClient import *

def main():
    client = FreeDriveClient()
    client.sync_file('testfile1.txt')

if __name__ == '__main__':
    main()
