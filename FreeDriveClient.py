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

from mimetypes import MimeTypes

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'config/client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
    
class FreeDriveClient():
    def __init__(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.drive = discovery.build('drive', 'v3', http=http)
    
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
    
    #Uploads a single file
    def upload(self, path, parent_id=None):       
        mime = MimeTypes()
        file_metadata = {'name': os.path.basename(path)}
        if parent_id:
            file_metadata['parents'] = [parent_id]
        try:
            media = MediaFileUpload(path, mimetype=mime.guess_type(os.path.basename(path))[0], resumable=True)
            file = self.drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
            return None
        except IOError as ioe:
            if (ioe.errno == 21):
                file_metadata = {
                    'name': path.split('/')[-1],
                    'mimeType': 'application/vnd.google-apps.folder',
                }

                if parent_id:
                    file_metadata['parent_id']

                file = self.drive.files().create(body=file_metadata, fields='id').execute() 
                return file.get('id')