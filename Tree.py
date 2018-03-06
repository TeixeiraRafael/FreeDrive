#coding: utf-8
from FreeDriveClient import *

class Node:
    def __init__(self, folder):
        self.name     = folder['name']
        self.folderId = folder['id']
        self.parents  = folder['parents']
        self.files    = []
        self.children = []
        
    def getId(self):
        return self.folderId


class Tree:
    def __init__(self, root=None):
        self.root = root
    
    def add(self, item):
        if(isinstance(item, Node)):
            self.addFolder(item)
        elif item['mimeType'] == 'application/vnd.google-apps.folder':
            n = Node(item)
            self.add(n)
        else:
            f_parents = item['parents']
            for parent in f_parents:
                parent_node = self.findFolder(parent)
                if parent_node != None:
                    parent_node.files.append(item)
                else:
                    print("add:\tNone.")

    def addFolder(self, folder):
        if self.root == None:
            self.root = folder
        else:
            f_parents = folder.parents
            print(f_parents[0])
            for parent in f_parents:
                parent_node = self.findFolder(parent)
                if(parent_node != None):
                    parent_node.children.append(folder)
                else:
                    print("addFolder:\tNone.")

    def findFolder(self, folderId, folder=None):
        if folder == None:
            self.root = folder

        if self.root != None:
            for f in root.children:
                if f.getId() == folderId:
                    return f
                self.findFolder(folderId, f)
            
    
    def showTree(self, root=None):
        if root == None:
            self.root = root
        else:
            print(root.name)
            for file in root.files:
                print("\t-" + file['name'])
            for folder in root.children:
                showTree(folder)

            