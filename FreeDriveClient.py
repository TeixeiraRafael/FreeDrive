#coding: utf-8
from __future__ import print_function
import httplib2

import os
import sys

from apiclient import discovery
from apiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import googleapiclient

import datetime
import time

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
            
            credentials = tools.run_flow(flow, store)
            
            print('Storing credentials to ' + credential_path)
        return credentials
    
    #Uploads a single file
    def upload(self, path, parent_id=None):       
        mime = MimeTypes()
        filename = path.split('/')[-1]
        file_metadata = {'name': filename}
        if parent_id:
            file_metadata['parents'] = [parent_id]
        try:
            media = MediaFileUpload(path, mimetype=mime.guess_type(os.path.basename(path))[0], resumable=True)
            file = self.drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
            return None
        except IOError as ioe:
            if (ioe.errno == 21):
                file_metadata = {'name': filename, 'mimeType': 'application/vnd.google-apps.folder'}
                if parent_id:
                    file_metadata['parents'] = [parent_id]
                file = self.drive.files().create(body=file_metadata, fields='id').execute()
                return file.get('id')
        
        except googleapiclient.errors.HttpError as err:
            return None
    
    def uploadFolder(self, folder):
        backup_date = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        backup_name = "backup " + str(backup_date)
        
        log_file = open(os.path.dirname(folder) + "/backup.log", 'w')
        log_file.write("Creating backup folder:\t"+backup_name + "\n")
        
        file_metadata = {'name': backup_name, 'mimeType': 'application/vnd.google-apps.folder'}
        file = self.drive.files().create(body=file_metadata, fields='id').execute()
        
        ids = {}
        ids[backup_name] = file.get('id')
        
        first_run = True

        for root, sub, files in os.walk(folder):
            if first_run:
                par = backup_name
            else:
                par = os.path.dirname(root)
            first_run = False

            file_metadata = {
                'name': os.path.basename(root),
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if par in ids.keys():
                file_metadata['parents'] = [ids[par]]
            
            log_file.write("Uploading:\t" + root + "\n")
            file = self.drive.files().create(body=file_metadata, fields='id').execute()
            id = file.get('id')
            ids[root] = id
            
            for f in files:
                log_file.write("Uploading:\t" + root + "/" + f + "\n")
                up = self.upload(root + '/' + f, id)
                if up == None:
                    log_file.write("\nError uploading file:\t" + root + "/" + f + "\n")
        
        current_time = datetime.datetime.now()
        log_file.write("\nBackup successfully finished at " + current_time.strftime('%d-%m-%Y %H:%M:%S') + "\n")
        
        return ids[backup_name]