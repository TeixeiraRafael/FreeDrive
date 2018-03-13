#coding: utf-8
from FreeDriveClient import *

def main():
    client = FreeDriveClient()
    print(client.upload("files/folder1/nested1/nested2"))
if __name__ == '__main__':
    main()
