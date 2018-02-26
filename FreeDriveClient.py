#coding: utf-8
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from apiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'config/client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
DEFAUTL_FOLDER = 'files/'
    
class FreeDriveClient():

    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                    'drive-python-quickstart.json')

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

        file_metadata = {'name': 'testfile.txt'}
        media = MediaFileUpload(DEFAUTL_FOLDER + filename, mimetype="text/txt")
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print("File's ID: %s" % file.get('id'))