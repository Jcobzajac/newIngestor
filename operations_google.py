from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from langchain_googledrive.document_loaders import GoogleDriveLoader

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def authentication(scope):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scope)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scope)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

#creds = authentication(SCOPES)

def modify_file(file_id_to_modify, file_name_with_new_content, creds):

    try:
        service = build('drive', 'v3', credentials=creds)

        media_content = MediaFileUpload(file_name_with_new_content,mimetype='text/plain')

        service.files().update(
            fileId=file_id_to_modify,
            media_body=media_content
        ).execute()

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


def get_file(file_id, file_name_local):

    loader = GoogleDriveLoader(file_ids=[file_id])
    docs = loader.load_and_split()
    
    try:
        content = docs[0].page_content
        with open(file_name_local, "w") as file:
            file.write(content)
    #If file is empty then provide also empty file
    except IndexError:
        with open(file_name_local, "w") as file:
            file.write("")




#modify_file(creds=authentication(SCOPES), file_id_to_modify="1LDWxIcNH9M5t21sdEpqyU3bQfXLp4ry_6AAhpQtBOfI", file_name_with_new_content="state.txt")

# "1LDWxIcNH9M5t21sdEpqyU3bQfXLp4ry_6AAhpQtBOfI" -- File id to modify




############ MAIN #############


#Get file with primary content

get_file(file_id="1o9pehABzLjkWy3ZLRALdjgGFIGPLIz7uS16toTUJRxo", file_name_local="primary.txt")

#Get file with summaries

get_file(file_id="1LDWxIcNH9M5t21sdEpqyU3bQfXLp4ry_6AAhpQtBOfI", file_name_local="summaries.txt")

# Get file with state

get_file(file_id="1MmRORzi6uGslMlBrHgx2rK36HZOX7KsE-a5LXL5hqV4", file_name_local="state.txt")






