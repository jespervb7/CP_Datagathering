import pickle
import os
import pandas as pd
import sys
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

def Create_Service(client_secret_file='client_secret.json', api_name='sheets', api_version='v4', scope = ['https://www.googleapis.com/auth/spreadsheets']):
    print(client_secret_file, api_name, api_version, scope, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = scope
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None
    
def write_to_sheet(data: list, range_to_write: str, client) -> None:
    """
    This function should write a list of lists to a certain sheet page

    - Data parameter 
        Takes a data or a list of lists
    - Data_range parameter
        This variable takes a string with the range of the sheet to write the data to. 
        An example would be: "Game_metadata!A1". 
        This should write to the Game_metadata sheet and it will automatically find it's way to add the data
    """
    
    # Validation for the right input
    if isinstance(data, list):
        print("Data validation succesful")
    else:
    # Transform dataframe to list of lists so that the data can be written to sheet
        print("Invalid datatype, should input a list")
        sys.exit()

    # Write to the sheet specified in the parameters
    request = client.spreadsheets().values().append(
        spreadsheetId="10_nr4Blz4z2kwdT0uIVsuo5Sy3mZSB-R5BPFP8A6B3o", 
        valueInputOption="RAW",
        range=range_to_write,
        body={
            'majorDimension': 'ROWS',
            'values': data
        })

    response = request.execute()

def read_from_sheet(sheet_name: str, client) -> list:
    """
    This function should read data from a google sheet to multiple pandas dataframes
    
    - Sheets parameter
        This variable takes a sheet name and will return a list
    """

    # Get's the data from a specific sheet
    request = client.spreadsheets().values().get(
        spreadsheetId="10_nr4Blz4z2kwdT0uIVsuo5Sy3mZSB-R5BPFP8A6B3o",
        majorDimension='ROWS',
        range=f"{sheet_name}!A1:Z1000000"
        ).execute()
    response = request['values']

    return response