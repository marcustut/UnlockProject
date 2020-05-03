"""
This python script is used to create folders for every game submission.
"""
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools


# define path variables
credentials_file_path = './credentials/credentials.json'
clientsecret_file_path = './credentials/client_secret.json'

# define API scope
SCOPE = 'https://www.googleapis.com/auth/drive'

# define store
store = file.Storage(credentials_file_path)
credentials = store.get()

# get access token
if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(clientsecret_file_path, SCOPE)
    credentials = tools.run_flow(flow, store)

# define API service
http = credentials.authorize(Http())
drive = discovery.build('drive', 'v3', http=http)

# test to create a folder


def create_folder(folder_name):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive.files().create(body=file_metadata, fields='id').execute()

    print("Folder ID: %s" % file.get('id'))


def create_insert_folder(folder_id, file_name):
    file_metadata = {
        'name': file_name,
        # mimeType is only required when inserting a folder
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folder_id]
    }
    file = drive.files().create(body=file_metadata, fields='id').execute()

    print(f"Folder ID: {file.get('id')}")


create_insert_folder('1xJid78X-HOf--dpagSl_ShocVhCTk2Mn', 'D1_Map')
