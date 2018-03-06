#coding: utf-8
from FreeDriveClient import *

def main():
    client = FreeDriveClient()
    client.build_tree()

if __name__ == '__main__':
    main()
