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
     
    def list_files(self, n):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)

        results = service.files().list(pageSize=n,fields="nextPageToken, files(name)").execute()
        
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(item['name'].encode('utf-8'))
    
    def upload(self, filename):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)

        file_metadata = {'name': filename, 'mimeType' : 'text/plain'}
        media = MediaFileUpload(self.sync_path + filename, mimetype="text/plain")
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        if file:
            return True
        else:
            print("Error uploading file: " + filename)
            return False

    def sync_file(self, filename):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)
        
        local_timestamp = os.path.getmtime(self.sync_path + filename)
        local_date = datetime.datetime.utcfromtimestamp(int(local_timestamp)).strftime('%Y-%m-%dT%H:%M:%S')
        page_token = None

        while True:
            response = service.files().list(q="modifiedTime < '" + str(local_date) + "'"
                                            + " and not trashed"
                                            + " and mimeType = 'text/plain'"
                                            + " and name = '" + filename + "'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name, mimeType, modifiedTime)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                file_metadata = {'name': filename, 'mimeType' : 'text/plain'}
                media = MediaFileUpload(self.sync_path + filename, mimetype="text/plain")

                update = service.files().update(fileId = file['id'], media_body=media).execute()

                if update:
                    print("Updated: " + filename)
                else:
                    print("Error updating file: " + filename)

            page_token = response.get('nextPageToken', None)
            if(page_token is None):
                break