#coding: utf-8
from FreeDriveClient import *
import os
import sys

def main():
    client = FreeDriveClient()
    indir = str(input())
    print(indir)
    parent = client.upload(indir)
    folders = []
    last_folder = parent
    for root, dirs, filenames in os.walk(indir):
        for f in filenames:
            client.upload(os.path.join(root, f), parent)
            print(os.path.join(root, f))
        for d in dirs:
            last_folder = client.upload(os.path.join(root, d), parent)
            print(os.path.join(root, d))
        parent = last_folder
        
            
            
if __name__ == '__main__':
    main()
