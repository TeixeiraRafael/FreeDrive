#coding: utf-8
from FreeDriveClient import *

def main():
    client = FreeDriveClient()
    print(client.get_folders())
    print(client.get_files())

if __name__ == '__main__':
    main()
