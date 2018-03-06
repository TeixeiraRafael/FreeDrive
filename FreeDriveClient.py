#coding: utf-8
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from apiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'config/client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
    
class FreeDriveClient():
    sync_path = 'files/'

    def __init__(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.drive = discovery.build('drive', 'v3', http=http)

    
    def set_syncPath(self, path):
        self.sync_path = path

    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)

        credential_path = os.path.join(credential_dir, 'drive-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
     
    def get_folders(self):
        folders = []
        page_token = None
        while True:
            response = self.drive.files().list(q="mimeType = 'application/vnd.google-apps.folder'", 
                                                fields="nextPageToken, files(id)", 
                                                pageToken=page_token).execute()
            for file in response.get('files', []):
                folders.append(file)

            page_token = response.get('nextPageToken', None)
            if(page_token is None):
                break
        return folders

    def get_files(self):
        files = []
        page_token = None
        while True:
            response = self.drive.files().list(q="mimeType != 'application/vnd.google-apps.folder'", 
                                                fields="nextPageToken, files(id)", 
                                                pageToken=page_token).execute()
            for file in response.get('files', []):
                files.append(file)

            page_token = response.get('nextPageToken', None)
            if(page_token is None):
                break
        return files


    def upload(self, filename):       
        filepath = filename.split('/')
        
        if(len(filepath) > 1):
            folder = filepath[-2]
            filename = filename[-1]
        else:
            folder = "My Drive"
            filename = filename[-1]


    def sync_file(self, filename):
        local_timestamp = os.path.getmtime(self.sync_path + filename)
        local_date = datetime.datetime.utcfromtimestamp(int(local_timestamp)).strftime('%Y-%m-%dT%H:%M:%S')
        page_token = None

        while True:
            response = self.drive.files().list(q="modifiedTime < '" + str(local_date) + "'"
                                            + " and not trashed"
                                            + " and mimeType = 'text/plain'"
                                            + " and name = '" + filename + "'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name, mimeType, modifiedTime)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                file_metadata = {'name': filename}
                media = MediaFileUpload(self.sync_path + filename, mimetype="text/plain")

                update = self.drive.files().update(fileId = file['id'], media_body=media).execute()

                if update:
                    print("Updated: " + filename)
                else:
                    print("Error updating file: " + filename)

            page_token = response.get('nextPageToken', None)
            if(page_token is None):
                break
    
    def browse(self):
        dirList = os.listdir("./"+self.sync_path)
        print(dirList)
    
    def get_parents(self, file):
        parent = self.drive.files().get(fileId = file['id']).execute()
        if file['parents']:
            print(1)
            get_parents(parent)
        else:
            return parent:


    def build_tree(self):
        pass